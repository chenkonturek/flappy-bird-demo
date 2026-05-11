## 1. GameConfig

- [x] 1.1 Add `sound_enabled: bool = True` field to `GameConfig` in `config.py`

## 2. SoundManager core

- [x] 2.1 Create `src/flappy_bird_demo/audio.py` with `SoundManager` class skeleton and `_enabled` flag
- [x] 2.2 Implement mixer initialisation in `__init__`: check `pygame.mixer.get_init()`, call `mixer.init()` only if not already running, wrap entire init block in `try/except Exception` that sets `self._enabled = False`
- [x] 2.3 Implement `_generate_square_wave(freq_hz, duration_s)` helper that returns a stereo `array.array('h', ...)` buffer using 44100 Hz sample rate
- [x] 2.4 Generate and store `self._flap` sound: 440 Hz square wave, 80 ms
- [x] 2.5 Generate and store `self._score` sound: 880 Hz (60 ms) concatenated with 1100 Hz (60 ms)
- [x] 2.6 Generate and store `self._death` sound: linear frequency sweep 400 Hz → 80 Hz over 400 ms (per-sample frequency interpolation)
- [x] 2.7 Generate and store `self._music` sound: four-note arpeggio C5-E5-G5-E5 (523/659/784/659 Hz), 500 ms per note, loop seam at phase zero
- [x] 2.8 Implement `play_flap() -> None`, `play_score() -> None`, `play_death() -> None` — each guards with `if not self._enabled: return`, then calls `sound.play()`
- [x] 2.9 Implement `start_music() -> None` — guards with `_enabled`, plays `self._music` on `self._music_channel` with `loops=-1`
- [x] 2.10 Implement `stop_music() -> None` — guards with `_enabled`, stops `self._music_channel` if it is not `None`
- [x] 2.11 Implement `close() -> None` — stops music channel; is a no-op when `_enabled` is `False`

## 3. CLI wiring

- [x] 3.1 Import `SoundManager` in `cli.py`
- [x] 3.2 Construct `SoundManager(config)` in `main()` alongside `Renderer` and `Game`
- [x] 3.3 Add `audio.close()` call to the `finally` block alongside `renderer.close()`
- [x] 3.4 Add pre-update snapshot variables: `prev_score = game.score.current` and `prev_state = game.state`
- [x] 3.5 Wire flap-during-GAME_OVER branch: call `game.reset()` then `audio.start_music()`
- [x] 3.6 Wire normal flap branch: call `game.handle_flap()` then `audio.play_flap()`
- [x] 3.7 Wire post-update death transition: if `game.state == GAME_OVER and prev_state == PLAYING`, call `audio.play_death()` then `audio.stop_music()`
- [x] 3.8 Wire post-update score event: if `game.score.current > prev_score`, call `audio.play_score()`

## 4. Tests

- [x] 4.1 Create `tests/test_audio.py`
- [x] 4.2 Write `test_sound_manager_disabled_no_exception`: construct `SoundManager(GameConfig(sound_enabled=False))`, assert no exception raised
- [x] 4.3 Write `test_play_methods_are_callable_when_disabled`: call all four play/start/stop methods on a disabled `SoundManager`, assert no exception
- [x] 4.4 Write `test_close_is_callable_when_disabled`: call `close()` on a disabled `SoundManager`, assert no exception
- [x] 4.5 Write `test_sound_enabled_default_true`: assert `GameConfig().sound_enabled is True`
- [x] 4.6 Write `test_sound_enabled_false`: assert `GameConfig(sound_enabled=False).sound_enabled is False`

## 5. New audio spec

- [x] 5.1 Create `openspec/specs/audio/spec.md` capturing the audio capability requirements (copy from change spec)

## 6. QA

- [x] 6.1 Run `just qa` — ruff format, ruff check, ty check, pytest all pass
- [x] 6.2 Manual smoke test: `uv run flappy_bird_demo` — flap sound, score ding, death buzz, and background music all audible
