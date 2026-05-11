## ADDED Requirements

### Requirement: sound_enabled controls audio initialisation
`GameConfig` has a `sound_enabled: bool = True` field. When `True`, `SoundManager` initialises `pygame.mixer` and generates sounds. When `False`, `SoundManager` skips all mixer work and all audio methods become no-ops. This field follows the same frozen/immutable rules as all other `GameConfig` fields.

#### Scenario: Default config enables sound
- **WHEN** `GameConfig()` is constructed with no arguments
- **THEN** `config.sound_enabled == True`

#### Scenario: Sound can be disabled at construction
- **WHEN** `GameConfig(sound_enabled=False)` is constructed
- **THEN** `config.sound_enabled == False`

#### Scenario: sound_enabled is immutable after construction
- **WHEN** code attempts to set `config.sound_enabled = False` on an existing instance
- **THEN** `FrozenInstanceError` is raised

## MODIFIED Requirements

### Requirement: Subsystems receive config by reference
`GameConfig` is passed to `Game`, `Renderer`, `Bird`, `Pipe`, `InputHandler`, and `SoundManager` at construction. They read from it but never write to it. The frozen constraint enforces this at the Python level.

#### Scenario: All subsystems share the same config instance
- **WHEN** `config = GameConfig()` is constructed once and passed to `Game(config)`, `Renderer(config)`, and `SoundManager(config)`
- **THEN** all three hold a reference to the same object (identity check passes)
