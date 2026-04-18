"""Tests for flappy_bird_demo.bird."""

import pytest

from flappy_bird_demo.bird import Bird
from flappy_bird_demo.config import GameConfig


@pytest.fixture
def config() -> GameConfig:
    return GameConfig()


@pytest.fixture
def bird(config: GameConfig) -> Bird:
    return Bird(x=config.bird_x, y=300.0, width=config.bird_width, height=config.bird_height)


def test_bird_initial_state(bird: Bird) -> None:
    assert bird.y == 300.0
    assert bird.velocity == 0.0


def test_bird_flap_sets_velocity(bird: Bird, config: GameConfig) -> None:
    bird.flap(config)
    assert bird.velocity == -config.flap_strength


def test_bird_falls_under_gravity(bird: Bird, config: GameConfig) -> None:
    initial_y = bird.y
    bird.update(config)
    assert bird.y > initial_y


def test_bird_does_not_go_above_screen(config: GameConfig) -> None:
    bird = Bird(x=config.bird_x, y=0.0, velocity=-10.0, width=config.bird_width, height=config.bird_height)
    bird.update(config)
    assert bird.y >= 0.0


def test_bird_hits_ground(config: GameConfig) -> None:
    ground_y = float(config.screen_height - config.bird_height)
    bird = Bird(x=config.bird_x, y=ground_y, width=config.bird_width, height=config.bird_height)
    assert bird.is_out_of_bounds(config) is True


def test_bird_rect(config: GameConfig) -> None:
    bird = Bird(x=80.7, y=200.3, width=config.bird_width, height=config.bird_height)
    assert bird.rect == (80, 200, config.bird_width, config.bird_height)


def test_bird_rect_dimensions_match_config(config: GameConfig) -> None:
    bird = Bird(x=config.bird_x, y=100.0, width=config.bird_width, height=config.bird_height)
    bx, by, bw, bh = bird.rect
    assert bw == config.bird_width
    assert bh == config.bird_height
    # renderer draws tail with ±5px and beak 8px wide — need bh//2 >= 5
    assert bh // 2 >= 5
