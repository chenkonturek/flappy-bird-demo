## ADDED Requirements

### Requirement: SoundManager generates all sounds at construction time
`SoundManager.__init__(config)` uses Python's stdlib `array` module to synthesise four chiptune sounds as 16-bit signed stereo PCM buffers and loads each into a `pygame.mixer.Sound` object. No external audio files are read from disk. All sounds are ready to play before the game loop starts.

#### Scenario: Sounds are available immediately after construction
- **WHEN** `SoundManager(config)` is constructed with `config.sound_enabled == True`
- **THEN** all four sounds (flap, score, death, background music) are loaded and playable without further I/O

---

### Requirement: Flap sound plays on every flap input during PLAYING
`SoundManager.play_flap()` plays an 80 ms square-wave blip at 440 Hz. It is called by `cli.py` immediately after `game.handle_flap()` when the game is in the `PLAYING` state.

#### Scenario: Flap sound is triggered on Space or click during play
- **WHEN** the player flaps while `game.state == PLAYING`
- **THEN** `play_flap()` is called and the 80 ms blip plays

---

### Requirement: Score sound plays each time a pipe is passed
`SoundManager.play_score()` plays a two-tone rising "ding" (880 Hz then 1100 Hz, 60 ms each). It is called by `cli.py` when `game.score.current` increments between the pre- and post-`update()` snapshots.

#### Scenario: Score sound fires exactly once per pipe passed
- **WHEN** `game.score.current` increases by 1 during `game.update()`
- **THEN** `play_score()` is called once

---

### Requirement: Death sound plays on transition to GAME_OVER
`SoundManager.play_death()` plays a 400 ms descending frequency sweep (400 Hz → 80 Hz). It is called by `cli.py` when `game.state` transitions from `PLAYING` to `GAME_OVER` during `game.update()`.

#### Scenario: Death sound fires on collision or ground hit
- **WHEN** `game.state` was `PLAYING` before `game.update()` and is `GAME_OVER` after
- **THEN** `play_death()` is called once

---

### Requirement: Background music loops continuously during PLAYING
`SoundManager.start_music()` plays a 2-second arpeggiated chiptune melody (C5-E5-G5-E5 square-wave loop) on a dedicated mixer channel with `loops=-1`. The music continues until `stop_music()` is called.

#### Scenario: Music starts on first flap
- **WHEN** the player flaps to transition from `IDLE` to `PLAYING`
- **THEN** `start_music()` is called and the background loop begins

#### Scenario: Music restarts on game reset
- **WHEN** the player flaps after `GAME_OVER`, triggering `game.reset()`, then flaps again to start a new game
- **THEN** `start_music()` is called again and the loop resumes from the beginning

---

### Requirement: Music stops on GAME_OVER
`SoundManager.stop_music()` halts the background music channel. It is called by `cli.py` immediately after the `PLAYING → GAME_OVER` transition is detected.

#### Scenario: Music is silenced when the bird dies
- **WHEN** `game.state` transitions to `GAME_OVER`
- **THEN** `stop_music()` is called and the music channel goes silent

---

### Requirement: SoundManager degrades to a no-op when mixer initialisation fails
If `pygame.mixer.init()` raises any exception, `SoundManager` sets `self._enabled = False` and all subsequent `play_*()`, `start_music()`, and `stop_music()` calls return immediately without error.

#### Scenario: Headless environment produces no exceptions
- **WHEN** `SoundManager(config)` is constructed in a headless environment where mixer init fails
- **THEN** no exception is raised and all audio methods are callable no-ops

#### Scenario: Disabled SoundManager does not affect game logic
- **WHEN** `SoundManager` is in the no-op state and `play_flap()` is called
- **THEN** the method returns without error and game state is unaffected

---

### Requirement: sound_enabled=False skips mixer initialisation entirely
When `config.sound_enabled == False`, `SoundManager.__init__` sets `self._enabled = False` without attempting to initialise `pygame.mixer` or generate any sounds.

#### Scenario: sound_enabled=False produces a fully no-op SoundManager
- **WHEN** `SoundManager(GameConfig(sound_enabled=False))` is constructed
- **THEN** `pygame.mixer` is never initialised and all methods are no-ops

---

### Requirement: SoundManager.close() releases the mixer channel
`SoundManager.close()` stops all active sounds on the managed channels. It is called in the `finally` block of `cli.main()` alongside `renderer.close()`.

#### Scenario: close() is called on exit
- **WHEN** the game loop exits for any reason
- **THEN** `audio.close()` is called, stopping any in-progress audio
