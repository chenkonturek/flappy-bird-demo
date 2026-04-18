# Plan: Flappy Bird Game in Python

## Context
The project is a scaffolded Python package (`flappy-bird-demo`) with `typer` + `rich` for CLI, `pytest` for testing, `ruff` for linting, and `ty` for type checking. The existing `cli.py` and `utils.py` are placeholder stubs. The goal is to implement a complete, playable Flappy Bird game following Python best practices and modular design.

## Approach: pygame-based game, logic decoupled from rendering

Add `pygame` as a dependency. Game logic (Bird, Pipe, Game state) is implemented as pure Python dataclasses/classes with **no pygame imports** — only `renderer.py` depends on pygame. This makes all game logic fully unit-testable without a display.

---

## Module Design

```
src/flappy_bird_demo/
├── config.py          # Dataclass of all game constants (gravity, speed, dimensions…)
├── bird.py            # Bird dataclass: position, velocity, flap(), update(), rect property
├── pipe.py            # Pipe dataclass: x, gap_y, move(), collides_with_bird(), passed_by()
├── score.py           # Score class: current, high_score, increment(), reset()
├── game.py            # Game class: state machine (IDLE→PLAYING→GAME_OVER), update loop
├── renderer.py        # Renderer class: pygame init/teardown, draw_frame(game_state)
├── input_handler.py   # InputHandler class: poll events → returns flap/quit signals
├── cli.py             # Updated: typer command launches Game + Renderer
└── utils.py           # Unchanged (kept for package compatibility)
```

### Key design decisions
- `Bird`, `Pipe`, `Score`, `Game` — **zero pygame imports**; testable in headless CI
- `Renderer` depends only on `Game` state snapshot (read-only); injectable/mockable
- `Config` is a frozen dataclass; pass it around rather than global constants
- `Game.update()` advances one tick; `Game.handle_flap()` is the only input entry point

---

## Files to Create / Modify

| File | Action | Notes |
|---|---|---|
| `pyproject.toml` | Modify | Add `pygame >= 2.5` to `[project] dependencies` |
| `src/flappy_bird_demo/config.py` | Create | `GameConfig` frozen dataclass |
| `src/flappy_bird_demo/bird.py` | Create | `Bird` dataclass + physics |
| `src/flappy_bird_demo/pipe.py` | Create | `Pipe` dataclass + generation helper |
| `src/flappy_bird_demo/score.py` | Create | `Score` class |
| `src/flappy_bird_demo/game.py` | Create | `GameState` enum + `Game` class |
| `src/flappy_bird_demo/renderer.py` | Create | `Renderer` class (pygame) |
| `src/flappy_bird_demo/input_handler.py` | Create | `InputHandler` class (pygame events) |
| `src/flappy_bird_demo/cli.py` | Modify | Replace stub with `run_game()` wiring |
| `src/flappy_bird_demo/utils.py` | Modify | Replace stub (or keep + add nothing) |

---

## Testing Plan

### Unit tests (no pygame required)

**`tests/test_bird.py`**
- `test_bird_initial_state` — y, velocity match config defaults
- `test_bird_flap_sets_velocity` — after `flap()`, velocity == -flap_strength
- `test_bird_falls_under_gravity` — `update()` increases y per gravity
- `test_bird_does_not_go_above_screen` — y clamped at 0
- `test_bird_hits_ground` — y >= screen_height → out-of-bounds flag
- `test_bird_rect` — `rect` property returns correct (x, y, w, h) tuple

**`tests/test_pipe.py`**
- `test_pipe_moves_left` — `move()` decreases x by speed
- `test_pipe_off_screen` — `is_off_screen()` True when x + width < 0
- `test_pipe_collision_inside_gap` — bird in gap → no collision
- `test_pipe_collision_top_section` — bird in top pipe → collision True
- `test_pipe_collision_bottom_section` — bird in bottom pipe → collision True
- `test_pipe_passed_by` — `passed_by(bird)` True when pipe.x + width < bird.x

**`tests/test_game.py`**
- `test_game_starts_idle` — initial state is `IDLE`
- `test_game_starts_on_first_flap` — `handle_flap()` in IDLE → state becomes PLAYING
- `test_game_over_on_pipe_collision` — update with overlapping pipe → GAME_OVER
- `test_game_over_on_ground_hit` — bird y >= screen_height → GAME_OVER
- `test_score_increments_on_pipe_pass` — pipe passed → score increases
- `test_game_resets_on_restart` — call `reset()` → back to IDLE, score 0
- `test_pipes_spawn_over_time` — after enough ticks new pipes added

**`tests/test_score.py`**
- `test_initial_score_zero`
- `test_increment_score`
- `test_reset_preserves_high_score`
- `test_high_score_updates_on_reset`

**`tests/test_config.py`**
- `test_config_defaults_are_positive` — gravity, speed, etc. > 0
- `test_config_screen_dimensions` — width/height > 0

### Integration / smoke tests

**`tests/test_integration.py`**
- `test_full_game_tick_sequence` — run N ticks, game reaches GAME_OVER eventually (no pipe gaps possible if bird never flaps)
- `test_game_survives_many_flaps` — rapid flaps don't crash or produce invalid state
- Renderer tests: skipped in CI via `pytest.mark.skipif(os.environ.get("CI"), ...)` since pygame needs a display

---

## Verification

1. `just qa` passes: ruff format + lint, ty check, pytest
2. `just coverage` ≥ 50% (game logic alone will exceed this; renderer excluded via `# pragma: no cover` on display-init lines)
3. Manual play: `uv run flappy_bird_demo` opens a pygame window, bird falls with gravity, spacebar flaps, pipes scroll, game over on collision, score displayed
