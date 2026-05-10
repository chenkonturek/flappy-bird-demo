# Capability: Bird Physics

The `Bird` dataclass in `bird.py` models the player-controlled bird. It tracks position, dimensions, and vertical velocity. It has no pygame dependency; all physics are pure arithmetic applied in `update()`.

---

### Requirement: Bird has a fixed horizontal position
The bird's `x` coordinate is set at construction and is never mutated by physics or game logic. Only `y` and `velocity` change during play.

#### Scenario: x does not change after update
- **WHEN** `Bird.update(config)` is called
- **THEN** `bird.x` is the same value it held before the call

---

### Requirement: Gravity accelerates the bird downward each tick
Each call to `Bird.update(config)` adds `config.gravity` to `velocity`, then adds the new `velocity` to `y`. Because the screen's positive-y axis points downward, positive velocity moves the bird toward the floor.

#### Scenario: Velocity increases after each tick
- **WHEN** `Bird.update(config)` is called on a bird with zero velocity
- **THEN** `bird.velocity` equals `config.gravity` and `bird.y` has increased

#### Scenario: Successive ticks accumulate velocity
- **WHEN** `Bird.update(config)` is called twice in a row
- **THEN** `bird.velocity` equals `2 * config.gravity` (default: 1.0) and `bird.y` has moved further than after one tick

---

### Requirement: Flap applies an upward velocity impulse
`Bird.flap(config)` sets `velocity` to `-config.flap_strength`, overwriting any current velocity. Negative velocity moves the bird toward the top of the screen.

#### Scenario: Flap sets velocity to negative flap_strength
- **WHEN** `Bird.flap(config)` is called
- **THEN** `bird.velocity == -config.flap_strength` (default: -8.0)

#### Scenario: Flap overrides downward velocity
- **WHEN** a bird that is already falling (positive velocity) calls `flap(config)`
- **THEN** `bird.velocity` becomes `-config.flap_strength` regardless of its previous value

---

### Requirement: The bird is clamped at the ceiling
If `update()` would move `y` below 0 (above the screen top), `y` is set to 0 and `velocity` is zeroed, preventing the bird from leaving the screen through the top.

#### Scenario: Ceiling clamp stops upward movement
- **WHEN** a bird at `y=0` with strong upward velocity (`velocity=-10.0`) calls `update(config)`
- **THEN** `bird.y >= 0.0` and `bird.velocity == 0.0`

---

### Requirement: Out-of-bounds detection signals ground collision
`Bird.is_out_of_bounds(config)` returns `True` when the bird's bottom edge (`y + height`) reaches or passes `config.screen_height`. It does not modify any state.

#### Scenario: Bird at the floor is out of bounds
- **WHEN** `bird.y == config.screen_height - config.bird_height`
- **THEN** `bird.is_out_of_bounds(config)` returns `True`

#### Scenario: Bird above the floor is not out of bounds
- **WHEN** `bird.y < config.screen_height - config.bird_height`
- **THEN** `bird.is_out_of_bounds(config)` returns `False`

---

### Requirement: The rect property returns an integer bounding box
`Bird.rect` is a computed property that returns `(int(x), int(y), width, height)`. Float positions are truncated to integers for collision math and rendering.

#### Scenario: Float coordinates are truncated to int
- **WHEN** `bird.x == 80.7` and `bird.y == 200.3`
- **THEN** `bird.rect == (80, 200, bird_width, bird_height)`

#### Scenario: Dimensions match config values
- **WHEN** a bird is created with `width=config.bird_width` and `height=config.bird_height`
- **THEN** `bird.rect[2] == config.bird_width` and `bird.rect[3] == config.bird_height`
