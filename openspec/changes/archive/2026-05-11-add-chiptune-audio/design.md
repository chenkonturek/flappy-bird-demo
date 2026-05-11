## Context

The game currently has no audio. All game logic (`game.py`, `bird.py`, `pipe.py`, `score.py`) is pure Python with zero pygame imports; only `renderer.py` imports pygame. This separation is a deliberate architectural constraint that must be preserved.

`pygame.mixer` is already available through the pygame-ce dependency and is initialised implicitly by `pygame.init()` (called inside `Renderer.__init__`). Sound generation requires no new runtime dependencies — the stdlib `array` module can produce the raw 16-bit signed sample buffers that `pygame.mixer.Sound` accepts.

## Goals / Non-Goals

**Goals:**
- Four audio events: flap, score, death, looping background music during play
- All sounds generated programmatically at startup — zero binary assets in the repo
- Graceful no-op when mixer initialisation fails (headless CI, no audio hardware)
- Audio on/off controlled by `GameConfig.sound_enabled`

**Non-Goals:**
- Volume control or mute toggle during play
- Loading external audio files
- Sound in `renderer.py` (visual and audio concerns stay separate)
- Changes to any pure-logic module (`game.py`, `bird.py`, `pipe.py`, `score.py`)

## Decisions

### Decision: New `audio.py` module, not extending `renderer.py`

`Renderer` is a visual concept. Mixing audio responsibility into it would surprise future readers and couple two independent concerns. A separate `SoundManager` in `audio.py` is the second pygame-importing module in the project, but the pygame isolation pattern (late import, `# pragma: no cover`, graceful try/except) is already established and straightforward to replicate.

**Alternative considered**: Fold into `renderer.py` — rejected because "renderer" is a visual word and the combined class would have no clean single responsibility.

### Decision: Programmatic chiptune generation via `array` module

All sounds are synthesised at `SoundManager` construction time using square waves built with Python's stdlib `array('h', ...)` (16-bit signed integers). `pygame.mixer.Sound(buffer=buf)` accepts this directly.

| Sound | Technique | Duration |
|---|---|---|
| Flap | 440 Hz square wave | 80 ms |
| Score | 880 Hz → 1100 Hz two-tone | 60 ms + 60 ms |
| Death | 400 Hz → 80 Hz linear frequency sweep | 400 ms |
| Background music | C5-E5-G5-E5 arpeggiated square-wave loop | 2 s (loops infinitely) |

Background music uses `Sound.play(loops=-1)` on a dedicated channel — no `pygame.mixer.music` (which requires a file on disk).

**Alternative considered**: Bundle `.ogg` files — rejected because it introduces binary blobs, licensing concerns, and package size growth with no quality benefit for a pixel-art game.

### Decision: Sound event detection in `cli.py`, not in `SoundManager`

`cli.py` already has full visibility into flap input (from `handler.poll()`) and can detect state/score transitions by comparing pre/post `game.update()` snapshots. Pushing event detection into `SoundManager` would require passing `game` state into it every frame, coupling it to `Game` internals. Instead, `cli.py` calls discrete `play_*()` and `start/stop_music()` methods.

### Decision: `pygame.mixer.get_init()` check before `mixer.init()`

`Renderer.__init__` calls `pygame.init()`, which initialises all pygame subsystems including the mixer. `SoundManager` checks `pygame.mixer.get_init()` before calling `mixer.init()` to avoid double-initialisation artefacts. If the mixer is already up, it skips init and proceeds directly to sound generation.

### Decision: `sound_enabled: bool = True` on `GameConfig`

A single boolean field on the frozen config makes audio trivially disableable for tests (`GameConfig(sound_enabled=False)`) and for future headless/automated runs. If `False`, `SoundManager.__init__` skips mixer init and all `play_*()` calls are no-ops — no try/except complexity needed at that level.

## Risks / Trade-offs

[Loop seam click] The 2-second background music buffer must end at the same waveform phase it started on, or there will be an audible click on each loop boundary. → Mitigation: generate the buffer length as an exact multiple of the lowest note's wavelength so the last sample's phase is 0.

[Mixer already initialised by Renderer] Calling `mixer.init()` when it is already running can reset mixer parameters. → Mitigation: check `pygame.mixer.get_init()` first; only call `mixer.init()` when the result is falsy.

[Channel exhaustion] pygame defaults to 8 mixing channels. We use one persistent channel for background music plus up to 3 transient SFX channels. Maximum concurrent sounds is 4, well within the default. → No mitigation needed.

[Headless CI] `pygame.mixer.init()` may raise or silently fail without audio hardware. → Mitigation: wrap the entire `__init__` body in `try/except Exception`; set `self._enabled = False` in the except branch so all methods become no-ops.

## Migration Plan

Backwards-compatible addition — no existing behaviour changes. `sound_enabled=True` is the default so existing callers of `GameConfig()` automatically get audio. No migration required.

To roll back: remove `audio.py`, remove `SoundManager` construction from `cli.py`, remove `sound_enabled` from `GameConfig`.

## Open Questions

None — all decisions resolved during exploration.
