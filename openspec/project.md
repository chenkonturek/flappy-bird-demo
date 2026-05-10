# Project: flappy-bird-demo

A terminal-playable Flappy Bird clone written in Python. The game runs in a pygame-ce window launched via a Typer CLI. The project doubles as a Python packaging reference: it uses a src-layout, ships `py.typed`, publishes to PyPI via SLSA-attested trusted publishing, and has a Zensical documentation site.

---

## Tech Stack

| Layer | Tool / Library |
|---|---|
| Language | Python 3.12–3.14 |
| Package / env manager | uv (`uv run`, `uv build`, `uv version`) |
| Task runner | just (`justfile`) |
| CLI framework | typer |
| Terminal output | rich (`rich.console.Console`) |
| Rendering | pygame-ce >= 2.5 |
| Linting / formatting | ruff (line-length 120; rules E, W, F, I, B, UP) |
| Type checker | ty (Astral) — all rules are errors by default |
| Testing | pytest + coverage (branch+parallel; `fail_under = 50`) |
| Documentation | Zensical + mkdocstrings-python (API reference auto-generated) |
| Build backend | hatchling |
| CI | GitHub Actions — lint → ty check → pytest matrix (3.12/3.13/3.14) → coverage combine |

---

## Repository Layout

```
src/
  flappy_bird_demo/
    __init__.py
    __main__.py          # re-exports app so `python -m flappy_bird_demo` works
    cli.py               # typer app; single `main` command; game loop lives here
    config.py            # GameConfig — frozen dataclass of all numeric constants
    game.py              # Game + GameState; pure logic, no pygame
    bird.py              # Bird dataclass; physics (gravity, flap)
    pipe.py              # Pipe dataclass + make_pipe factory; scrolling obstacles
    score.py             # Score class; current + high score tracking
    renderer.py          # Renderer; only module that imports pygame
    input_handler.py     # InputHandler; reads keyboard/mouse, returns (flap, quit)
    utils.py             # Cross-cutting helpers only — not a catch-all
    py.typed             # PEP 561 marker
tests/
  test_bird.py
  test_config.py
  test_flappy_bird_demo.py
  test_game.py
  test_integration.py
  test_pipe.py
  test_score.py
scripts/
  release.py             # PEP 723 standalone script; tags, pushes, creates GitHub release
docs/                    # Zensical site
CHANGELOG/<version>.md   # Per-release notes; first `# ` line becomes release title
openspec/
  changes/               # Active and archived change proposals
  specs/                 # Capability specifications
```

---

## Architecture Patterns

### Separation of concerns
All game logic (`game.py`, `bird.py`, `pipe.py`, `score.py`) has **zero pygame imports**. Only `renderer.py` imports pygame. This allows the full logic layer to be tested without a display.

### Game loop (in `cli.py`)
```
IDLE → (first flap) → PLAYING → (collision / out-of-bounds) → GAME_OVER → (flap) → IDLE
```
`InputHandler.poll()` returns `(flap: bool, quit: bool)`. `Game.update()` advances simulation by one tick. `Renderer.draw_frame(game)` renders the current state. `Renderer.tick(fps)` caps the loop.

### Configuration via frozen dataclass
All numeric game constants live in `GameConfig` (`@dataclass(frozen=True)`). No bare magic numbers in logic files. Mutable game entities (`Bird`, `Pipe`) use plain `@dataclass`.

### Module-level constants
Non-config constants use `SCREAMING_SNAKE_CASE` at the top of their module.

---

## Coding Conventions

### Type annotations
- All public functions and methods require full annotations including `-> None`.
- Use native union syntax (`X | Y`, `list[X]`); Python floor is 3.12 so no `from __future__ import annotations`.
- Prefer concrete types over `Any`; comment why if `Any` is unavoidable.

### Docstrings — Google Python Style
- Every public module, class, and function needs a one-line imperative summary ("Return …", "Apply …").
- Multi-line: use `Args:`, `Returns:`, `Raises:`, `Attributes:` sections.
- Class docstrings include `Attributes:` for non-obvious fields.
- Omit `Args:`/`Returns:` when they would only restate the type annotation.
- Private helpers (`_name`) skip docstrings unless logic is subtle.

### Terminal output
- Use `rich.console.Console` — never bare `print()` in library code.

### Error handling
- Raise `ValueError` / `TypeError` at public API boundaries with a descriptive message.
- Never swallow exceptions silently; re-raise or log.
- Return meaningful values; avoid `None` to signal failure — raise instead.

### No unnecessary abstractions
- Don't pre-emptively abstract; three similar lines beat a premature helper.
- `utils.py` is for genuinely cross-cutting helpers only.

---

## Test Conventions

- Mirror structure: `tests/test_<module>.py` per source module.
- Use `pytest.mark.parametrize` for table-driven cases.
- Test names: `test_<unit>_<scenario>` (e.g. `test_bird_falls_with_gravity`).
- **Do not mock internal game logic.** Test real objects using `GameConfig` defaults.
- `Renderer` and `InputHandler` are excluded from coverage (`# pragma: no cover`) because they require a display.

---

## Development Workflow

```bash
just qa          # full local gate before committing
just test        # pytest on Python 3.14
just testall     # pytest on 3.12, 3.13, 3.14
just type-check  # ty check
just coverage    # branch+parallel coverage across all Pythons
just docs-serve  # live-reload Zensical site on :8000
just build       # produces dist/ artifacts
```

CI runs `just qa` equivalent steps; keep it green locally before pushing.

---

## Constraints

- **Python floor is 3.12.** Avoid syntax or stdlib that breaks on 3.12.
- **No bare `print()`** in any library or CLI code — use `rich`.
- **`renderer.py` is the only pygame import site.** All other modules must remain pygame-free.
- **GameConfig is the single source of truth** for numeric constants; no duplicate literals.
- **Coverage threshold: 50%.** New features should maintain or improve coverage.
- **Ruff is the formatter** — do not hand-format; always run `ruff format` via `just qa`.

---

## Release Flow

1. `uv version <version>` — bumps `pyproject.toml`
2. Write `CHANGELOG/<version>.md` (first `# ` heading becomes the GitHub release title)
3. Commit `pyproject.toml`, `uv.lock`, changelog entry with message `Release <version>`
4. `just release` — tags, pushes, creates GitHub Release; CI publishes to PyPI via trusted publishing with SLSA provenance
