## Why

The game has no audio, which makes it feel flat and less engaging. Adding chiptune sound effects and background music (programmatically generated — no binary assets required) will improve game feel and complete the core gameplay experience described in issue #14.

## What Changes

- **New module `audio.py`**: `SoundManager` class that generates all sounds at construction time using pure Python (`array` module + pygame mixer). No external audio files.
- **New `sound_enabled` field on `GameConfig`**: `bool`, defaults to `True`. Allows silent mode for tests and CI.
- **Updated `cli.py`**: Constructs `SoundManager`, wires flap/score/death sound triggers and background music lifecycle into the game loop.
- **New spec `openspec/specs/audio/spec.md`**: Documents the audio capability requirements.

No changes to `game.py`, `bird.py`, `pipe.py`, `score.py`, or `renderer.py`.

## Capabilities

### New Capabilities

- `audio`: Programmatically generated chiptune sound effects and looping background music, driven by game state transitions detected in the CLI game loop. Gracefully degrades to a no-op when pygame mixer is unavailable (headless CI).

### Modified Capabilities

- `game-config`: `sound_enabled: bool = True` field is added. This is a spec-level change — callers can now control audio at construction time.
- `cli`: The game loop gains three new responsibilities: triggering sound events on flap input and state transitions, managing background music lifecycle (start on PLAYING, stop on GAME_OVER, restart on reset).

## Impact

- **`src/flappy_bird_demo/audio.py`**: new file
- **`src/flappy_bird_demo/config.py`**: one new field
- **`src/flappy_bird_demo/cli.py`**: game loop updated
- **`tests/test_audio.py`**: new test file (uses `GameConfig(sound_enabled=False)` to skip mixer init)
- **No new runtime dependencies**: `array` is stdlib; pygame-ce is already a dependency
- **CI**: no display or audio hardware required — graceful no-op path in `SoundManager.__init__`