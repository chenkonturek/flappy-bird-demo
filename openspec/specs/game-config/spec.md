# Capability: Game Configuration

`GameConfig` (in `config.py`) is a frozen dataclass that centralises every numeric constant used by the game. It is created once in `cli.py` and passed by reference to all subsystems. Because it is frozen, no subsystem can accidentally mutate the configuration at runtime.

---

### Requirement: GameConfig is immutable after construction
`GameConfig` uses `@dataclass(frozen=True)`. Any attempt to assign to a field after construction raises `FrozenInstanceError`.

#### Scenario: Attribute assignment raises an error
- **WHEN** code attempts to set `config.gravity = 1.0` on an existing instance
- **THEN** `FrozenInstanceError` is raised

---

### Requirement: All numeric fields have positive default values
Every numeric field's default is greater than zero. This prevents degenerate states such as zero gravity or a zero-width screen.

#### Scenario: Default config has all-positive values
- **WHEN** `GameConfig()` is constructed with no arguments
- **THEN** `gravity > 0`, `pipe_speed > 0`, `flap_strength > 0`, `pipe_gap > 0`, `fps > 0`, `screen_width > 0`, `screen_height > 0`

---

### Requirement: Default values match the canonical game parameters
The defaults encode the intended gameplay feel. Changing them changes game difficulty.

| Field | Default | Meaning |
|---|---|---|
| `screen_width` | 400 | Window width in pixels |
| `screen_height` | 600 | Window height in pixels |
| `gravity` | 0.5 | Downward acceleration per tick (pixels/tick²) |
| `flap_strength` | 8.0 | Upward velocity applied on each flap (pixels/tick) |
| `pipe_speed` | 3.0 | Pixels a pipe moves left per tick |
| `pipe_gap` | 150 | Height of the passable opening in pixels |
| `pipe_width` | 60 | Width of each pipe in pixels |
| `pipe_spawn_interval` | 90 | Ticks between consecutive pipe spawns |
| `bird_x` | 80 | Fixed horizontal pixel position of the bird |
| `bird_width` | 34 | Bird sprite width in pixels |
| `bird_height` | 24 | Bird sprite height in pixels |
| `fps` | 60 | Target frames per second |

#### Scenario: Default screen dimensions are 400×600
- **WHEN** `GameConfig()` is constructed
- **THEN** `config.screen_width == 400` and `config.screen_height == 600`

#### Scenario: Default bird dimensions allow safe tail rendering
- **WHEN** `GameConfig()` is constructed
- **THEN** `config.bird_height // 2 >= 5` (renderer draws tail with ±5 px offset)

---

### Requirement: Subsystems receive config by reference
`GameConfig` is passed to `Game`, `Renderer`, `Bird`, `Pipe`, and `InputHandler` at construction. They read from it but never write to it. The frozen constraint enforces this at the Python level.

#### Scenario: All subsystems share the same config instance
- **WHEN** `config = GameConfig()` is constructed once and passed to `Game(config)` and `Renderer(config)`
- **THEN** both hold a reference to the same object (identity check passes)
