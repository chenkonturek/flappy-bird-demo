"""Chiptune audio — one of two modules that import pygame."""

import array
from typing import Any

from flappy_bird_demo.config import GameConfig

_SAMPLE_RATE = 44100
_AMPLITUDE = 8000


def _square_wave(freq_hz: float, duration_s: float) -> array.array[int]:
    """Return a stereo signed-16-bit square-wave buffer.

    Args:
        freq_hz: Tone frequency in Hz.
        duration_s: Duration in seconds.

    Returns:
        Interleaved left/right 16-bit samples as an ``array.array('h')``.
    """
    n = int(_SAMPLE_RATE * duration_s)
    buf: array.array[int] = array.array("h")
    for i in range(n):
        v = _AMPLITUDE if (i * freq_hz / _SAMPLE_RATE) % 1.0 < 0.5 else -_AMPLITUDE
        buf.append(v)
        buf.append(v)
    return buf


def _sweep(freq_start: float, freq_end: float, duration_s: float) -> array.array[int]:
    """Return a stereo signed-16-bit linearly-swept square-wave buffer.

    Args:
        freq_start: Starting frequency in Hz.
        freq_end: Ending frequency in Hz.
        duration_s: Duration in seconds.

    Returns:
        Interleaved left/right 16-bit samples as an ``array.array('h')``.
    """
    n = int(_SAMPLE_RATE * duration_s)
    buf: array.array[int] = array.array("h")
    phase = 0.0
    for i in range(n):
        freq = freq_start + (freq_end - freq_start) * i / n
        phase += freq / _SAMPLE_RATE
        v = _AMPLITUDE if phase % 1.0 < 0.5 else -_AMPLITUDE
        buf.append(v)
        buf.append(v)
    return buf


def _music_loop() -> array.array[int]:
    """Return a seamless looping C5-E5-G5-E5 arpeggio buffer.

    Each note uses an integer number of complete wavelengths closest to 500 ms
    so the loop boundary lands at phase zero and avoids an audible click.

    Returns:
        Interleaved left/right 16-bit samples as an ``array.array('h')``.
    """
    buf: array.array[int] = array.array("h")
    amp = _AMPLITUDE // 2  # quieter than SFX so music stays in background
    for freq in (523, 659, 784, 659):  # C5, E5, G5, E5
        cycles = round(freq * 0.5)  # nearest whole-cycle count to ~500 ms
        n = int(_SAMPLE_RATE * cycles / freq)
        for i in range(n):
            v = amp if (i * freq / _SAMPLE_RATE) % 1.0 < 0.5 else -amp
            buf.append(v)
            buf.append(v)
    return buf


class SoundManager:  # pragma: no cover
    """Generate and play chiptune sound effects and looping background music.

    All sounds are synthesised at construction from pure Python buffers — no
    audio files are loaded. When ``config.sound_enabled`` is ``False``, or when
    ``pygame.mixer`` fails to initialise, every method becomes a no-op.

    Attributes:
        _enabled: Whether the mixer initialised successfully and audio is active.
        _music_channel: Active ``pygame.mixer.Channel`` for the looping music, or ``None``.
    """

    def __init__(self, config: GameConfig) -> None:
        """Initialise pygame mixer and pre-generate all chiptune sounds.

        Args:
            config: Game configuration; ``sound_enabled=False`` skips all mixer work.
        """
        self._enabled = False
        self._music_channel: Any = None  # pygame.mixer.Channel; Any avoids late-import typing

        if not config.sound_enabled:
            return

        try:
            import pygame  # noqa: PLC0415

            self._pygame = pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=_SAMPLE_RATE, size=-16, channels=2, buffer=512)

            self._flap = pygame.mixer.Sound(buffer=_square_wave(440, 0.08))

            score_buf = _square_wave(880, 0.06)
            score_buf.extend(_square_wave(1100, 0.06))
            self._score = pygame.mixer.Sound(buffer=score_buf)

            self._death = pygame.mixer.Sound(buffer=_sweep(400, 80, 0.4))
            self._music = pygame.mixer.Sound(buffer=_music_loop())
            self._enabled = True
        except Exception:
            self._enabled = False

    def play_flap(self) -> None:
        """Play the 80 ms wing-flap blip (440 Hz square wave)."""
        if not self._enabled:
            return
        self._flap.play()

    def play_score(self) -> None:
        """Play the two-tone rising score ding (880 Hz then 1100 Hz)."""
        if not self._enabled:
            return
        self._score.play()

    def play_death(self) -> None:
        """Play the 400 ms descending death buzz (400 Hz → 80 Hz sweep)."""
        if not self._enabled:
            return
        self._death.play()

    def start_music(self) -> None:
        """Start looping the background arpeggiated melody."""
        if not self._enabled:
            return
        self._music_channel = self._music.play(loops=-1)

    def stop_music(self) -> None:
        """Stop the background music channel immediately."""
        if not self._enabled:
            return
        if self._music_channel is not None:
            self._music_channel.stop()
            self._music_channel = None

    def close(self) -> None:
        """Stop all managed audio channels."""
        self.stop_music()
