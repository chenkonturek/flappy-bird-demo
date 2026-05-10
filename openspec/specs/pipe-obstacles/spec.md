# Capability: Pipe Obstacles

`Pipe` (in `pipe.py`) is a mutable dataclass that represents a single scrolling obstacle. Each pipe has a top segment (from y=0 to `gap_y`) and a bottom segment (from `gap_y + gap` to the screen floor), with a passable opening between them. `make_pipe()` is the factory used by the game to spawn new pipes. There is no pygame dependency.

---

### Requirement: Pipes scroll left at a configurable speed
Each call to `Pipe.move(config)` decreases `x` by `config.pipe_speed`. The horizontal position is a float; the renderer truncates to int for drawing.

#### Scenario: x decreases by pipe_speed each tick
- **WHEN** `Pipe.move(config)` is called on a pipe at `x=300.0`
- **THEN** `pipe.x == 300.0 - config.pipe_speed`

---

### Requirement: Off-screen detection triggers when the pipe exits the left edge
`Pipe.is_off_screen()` returns `True` when the pipe's right edge (`x + width`) is strictly less than 0 — meaning the entire pipe has scrolled past the left boundary.

#### Scenario: Pipe fully past left edge is off-screen
- **WHEN** `pipe.x == -(config.pipe_width + 1)`
- **THEN** `pipe.is_off_screen()` returns `True`

#### Scenario: Pipe partially or fully on screen is not off-screen
- **WHEN** `pipe.x == 300.0` (well within screen)
- **THEN** `pipe.is_off_screen()` returns `False`

---

### Requirement: Collision detection uses axis-aligned bounding-box overlap
`Pipe.collides_with(bird_rect)` returns `True` when the bird overlaps the top or bottom pipe segment. The check is purely rectangular; there is no pixel-perfect detection.

The algorithm:
1. If there is no horizontal overlap between the bird rect and the pipe, return `False`.
2. If the bird's top edge (`bird_y`) is above `gap_y`, it overlaps the top segment → return `True`.
3. If the bird's bottom edge (`bird_y + bird_height`) is below `gap_y + gap`, it overlaps the bottom segment → return `True`.
4. Otherwise the bird is within the gap → return `False`.

#### Scenario: Bird inside the gap does not collide
- **WHEN** the bird rect is entirely within the opening (y=210, height=24, gap at 200–350)
- **THEN** `pipe.collides_with(bird_rect)` returns `False`

#### Scenario: Bird overlapping the top segment collides
- **WHEN** `bird_y=180` with `gap_y=200` (bird top is above the gap)
- **THEN** `pipe.collides_with(bird_rect)` returns `True`

#### Scenario: Bird overlapping the bottom segment collides
- **WHEN** `bird_y=340`, `bird_height=24` (bottom edge 364 > 350 = gap_y + gap)
- **THEN** `pipe.collides_with(bird_rect)` returns `True`

#### Scenario: Bird with no horizontal overlap does not collide
- **WHEN** `bird_x + bird_width <= pipe.x` (bird is entirely to the left of the pipe)
- **THEN** `pipe.collides_with(bird_rect)` returns `False`

---

### Requirement: Passed-by detection fires once the bird clears the pipe's right edge
`Pipe.passed_by(bird_rect)` returns `True` when the bird's leading edge (`bird_x`) is strictly greater than the pipe's right edge (`pipe.x + pipe.width`).

#### Scenario: Bird to the right of the pipe's right edge is "passed"
- **WHEN** `bird_x > pipe.x + pipe.width`
- **THEN** `pipe.passed_by(bird_rect)` returns `True`

---

### Requirement: make_pipe spawns a new pipe entering from the right
`make_pipe(config, screen_width)` creates a `Pipe` with:
- `x = float(screen_width)` — starts just off the right edge
- `width = config.pipe_width`
- `gap = config.pipe_gap`
- `gap_y` chosen uniformly at random from `[80, config.screen_height - config.pipe_gap - 80]`

The 80-pixel margin on each side ensures the opening is always reachable; the gap centre is never too close to the top or bottom edge.

#### Scenario: New pipe starts at the right edge of the screen
- **WHEN** `make_pipe(config, config.screen_width)` is called
- **THEN** `pipe.x == float(config.screen_width)`

#### Scenario: New pipe uses config dimensions
- **WHEN** `make_pipe(config, config.screen_width)` is called
- **THEN** `pipe.width == config.pipe_width` and `pipe.gap == config.pipe_gap`

#### Scenario: Gap position is within the safe margin
- **WHEN** `make_pipe(config, config.screen_width)` is called
- **THEN** `80 <= pipe.gap_y <= config.screen_height - config.pipe_gap - 80`
