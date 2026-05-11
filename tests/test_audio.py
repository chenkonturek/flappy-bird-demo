"""Tests for flappy_bird_demo.audio."""


from flappy_bird_demo.audio import SoundManager
from flappy_bird_demo.config import GameConfig


def test_sound_manager_disabled_no_exception() -> None:
    SoundManager(GameConfig(sound_enabled=False))


def test_play_methods_are_callable_when_disabled() -> None:
    audio = SoundManager(GameConfig(sound_enabled=False))
    audio.play_flap()
    audio.play_score()
    audio.play_death()
    audio.start_music()
    audio.stop_music()


def test_close_is_callable_when_disabled() -> None:
    audio = SoundManager(GameConfig(sound_enabled=False))
    audio.close()


def test_sound_enabled_default_true() -> None:
    assert GameConfig().sound_enabled is True


def test_sound_enabled_false() -> None:
    assert GameConfig(sound_enabled=False).sound_enabled is False
