## MODIFIED Requirements

### Requirement: The main command initialises all subsystems from a shared config
`main()` constructs `GameConfig`, `Game(config)`, `Renderer(config)`, `InputHandler()`, and `SoundManager(config)` before entering the game loop. All subsystems share the same `GameConfig` instance.

#### Scenario: Subsystems constructed from one config
- **WHEN** `main()` is called
- **THEN** `Game`, `Renderer`, `InputHandler`, and `SoundManager` are all initialised before the loop begins

---

### Requirement: The game loop polls input, updates state, and renders on every frame
Each iteration of the loop follows this fixed order:
1. `handler.poll()` → `(flap, quit_)`
2. If `quit_` is `True`, break out of the loop.
3. Snapshot `prev_score = game.score.current` and `prev_state = game.state`.
4. If `flap` is `True` and `game.state == GAME_OVER`, call `game.reset()` and `audio.start_music()`.
5. Else if `flap` is `True`, call `game.handle_flap()` and `audio.play_flap()`.
6. `game.update()`
7. If `game.state == GAME_OVER` and `prev_state == PLAYING`, call `audio.play_death()` and `audio.stop_music()`.
8. If `game.score.current > prev_score`, call `audio.play_score()`.
9. `renderer.draw_frame(game)`
10. `renderer.tick(config.fps)`

#### Scenario: Loop processes one frame per iteration
- **WHEN** the game loop runs
- **THEN** poll → snapshot → input handling → update → audio events → draw → tick happen in that order every iteration

#### Scenario: Flap sound plays on each flap during PLAYING
- **WHEN** the player flaps while `game.state == PLAYING`
- **THEN** `audio.play_flap()` is called on that frame

#### Scenario: Score sound plays when a pipe is passed
- **WHEN** `game.score.current` increases during `game.update()`
- **THEN** `audio.play_score()` is called on that frame

#### Scenario: Death sound plays and music stops on GAME_OVER
- **WHEN** `game.state` transitions from `PLAYING` to `GAME_OVER` during `game.update()`
- **THEN** `audio.play_death()` and `audio.stop_music()` are both called on that frame

#### Scenario: Music restarts when player resets
- **WHEN** `flap` is `True` while `game.state == GAME_OVER`
- **THEN** `game.reset()` and `audio.start_music()` are called (music resumes for the new session)

## ADDED Requirements

### Requirement: audio.close() is always called on exit
`main()` calls `audio.close()` in the `finally` block alongside `renderer.close()`, ensuring all mixer channels are stopped whether the loop exits normally or via an exception.

#### Scenario: Audio is closed after the loop
- **WHEN** the game loop exits for any reason
- **THEN** `audio.close()` is called exactly once
