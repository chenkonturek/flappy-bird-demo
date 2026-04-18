"""Tests for flappy_bird_demo.config."""

import pytest

from flappy_bird_demo.config import GameConfig


@pytest.fixture
def config() -> GameConfig:
    return GameConfig()


def test_config_defaults_are_positive(config: GameConfig) -> None:
    assert config.gravity > 0
    assert config.pipe_speed > 0
    assert config.flap_strength > 0
    assert config.pipe_gap > 0
    assert config.fps > 0


def test_config_screen_dimensions(config: GameConfig) -> None:
    assert config.screen_width > 0
    assert config.screen_height > 0
