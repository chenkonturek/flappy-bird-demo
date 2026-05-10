# Capability: Game Loop

`Game` (in `game.py`) coordinates all entities and enforces the rules of play. It owns the `Bird`, a list of active `Pipe` obstacles, and a `Score`. It exposes three methods — `handle_flap()`, `update()`, and `reset()` — that are called by the CLI on every frame. There is no pygame dependency.

---

### Requirement: The game starts in the IDLE state
A freshly constructed `Game` instance is in `GameState.IDLE`. No physics run until the player flaps.

#### Scenario: New game is idle
- **WHEN** `Game(config)` is constructed
- **THEN** `game.state == GameState.IDLE`

---

### Requirement: The first flap transitions IDLE to PLAYING
`Game.handle_flap()` called while `state == IDLE` sets the state to `PLAYING` and applies a flap impulse to the bird.

#### Scenario: First flap starts the game
- **WHEN** `game.handle_flap()` is called on an IDLE game
- **THEN** `game.state == GameState.PLAYING`

---

### Requirement: Flap during PLAYING applies a velocity impulse without changing state
`Game.handle_flap()` called while `state == PLAYING` applies a flap to the bird but leaves the state as `PLAYING`.

#### Scenario: Flap during play does not change state
- **WHEN** `game.handle_flap()` is called on a PLAYING game
- **THEN** `game.state == GameState.PLAYING`

---

### Requirement: handle_flap is a no-op during GAME_OVER
`Game.handle_flap()` called while `state == GAME_OVER` has no effect on state or the bird. The CLI triggers `game.reset()` instead.

#### Scenario: Flap during game-over does nothing
- **WHEN** `game.handle_flap()` is called on a GAME_OVER game
- **THEN** `game.state == GameState.GAME_OVER` and the bird is unchanged

---

### Requirement: update() is a no-op when not PLAYING
`Game.update()` returns immediately if `state != PLAYING`. Pipes are not moved, the bird is not updated, and the tick counter does not advance.

#### Scenario: update does nothing in IDLE
- **WHEN** `game.update()` is called while `state == IDLE`
- **THEN** `game.state == GameState.IDLE` and no pipes have spawned

#### Scenario: update does nothing in GAME_OVER
- **WHEN** `game.update()` is called while `state == GAME_OVER`
- **THEN** `game.state == GameState.GAME_OVER`

---

### Requirement: Pipes spawn on a fixed tick interval starting at tick 0
While PLAYING, `update()` spawns a new pipe whenever `tick_count % pipe_spawn_interval == 0`. This fires at tick 0 (the very first update call), then again at ticks 90, 180, … (with default config).

#### Scenario: A pipe is present immediately after the first update
- **WHEN** `game.update()` is called for the first time while PLAYING
- **THEN** `len(game.pipes) >= 1`

#### Scenario: Subsequent pipes spawn at configured intervals
- **WHEN** `game.update()` is called `pipe_spawn_interval + 1` times while PLAYING
- **THEN** at least two pipes have existed (the second spawned at tick `pipe_spawn_interval`)

---

### Requirement: Pipe collision triggers GAME_OVER
If any active pipe's `collides_with(bird_rect)` returns `True` during `update()`, the state transitions to `GAME_OVER` and the update returns immediately (no further checks that tick).

#### Scenario: Overlapping pipe ends the game
- **WHEN** a pipe is placed directly on the bird's position and `game.update()` is called
- **THEN** `game.state == GameState.GAME_OVER`

---

### Requirement: Ground or ceiling exit triggers GAME_OVER
If `bird.is_out_of_bounds(config)` returns `True` after the bird has been updated, the state transitions to `GAME_OVER`.

#### Scenario: Bird falling below the screen ends the game
- **WHEN** the bird's y is set to `config.screen_height - bird.height` and `game.update()` is called
- **THEN** `game.state == GameState.GAME_OVER`

---

### Requirement: Each pipe is scored exactly once when the bird passes it
After a pipe's `passed_by(bird_rect)` returns `True`, `score.increment()` is called and the pipe's id is recorded in `_counted_pipe_ids`. Subsequent ticks do not count the same pipe again. When a pipe scrolls off screen its id is removed from `_counted_pipe_ids` to prevent unbounded growth.

#### Scenario: Score increments when a pipe is passed
- **WHEN** a pipe is positioned just behind the bird and `game.update()` is called
- **THEN** `game.score.current > 0`

#### Scenario: Passing the same pipe twice does not double-count
- **WHEN** `game.update()` is called multiple times after a pipe has been passed
- **THEN** `game.score.current == 1` (counted once)

---

### Requirement: Off-screen pipes are removed from the active list each tick
During `update()`, any pipe for which `is_off_screen()` returns `True` is dropped from `game.pipes`. Its id is also removed from `_counted_pipe_ids`.

#### Scenario: Pipe that has scrolled off is removed
- **WHEN** a pipe is moved to `x = -(pipe_width + 1)` and `game.update()` is called
- **THEN** that pipe is no longer in `game.pipes`

---

### Requirement: reset() restores a clean IDLE state while preserving the high score
`Game.reset()` calls `score.reset()` (which saves the high score), creates a fresh `Bird` at the centre of the screen, empties the pipe list, zeroes `tick_count`, clears `_counted_pipe_ids`, and sets `state` to `IDLE`.

#### Scenario: State returns to IDLE after reset
- **WHEN** `game.reset()` is called on a GAME_OVER game
- **THEN** `game.state == GameState.IDLE`

#### Scenario: Current score is cleared after reset
- **WHEN** `game.reset()` is called after accumulating points
- **THEN** `game.score.current == 0`

#### Scenario: High score is retained after reset
- **WHEN** `game.reset()` is called after reaching a score of N
- **THEN** `game.score.high >= N`

#### Scenario: Pipes are cleared after reset
- **WHEN** `game.reset()` is called while pipes are on screen
- **THEN** `game.pipes == []`

---

### Requirement: The game reaches GAME_OVER without input within a finite time
A bird that receives no flap input will fall under gravity and eventually hit the ground. This SHALL happen within 2000 ticks.

#### Scenario: No-input game ends naturally
- **WHEN** the game is started with a single flap then `update()` is called with no further input
- **THEN** `game.state == GameState.GAME_OVER` within 2000 ticks
