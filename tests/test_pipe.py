"""Tests for flappy_bird_demo.pipe."""

import pytest

from flappy_bird_demo.config import GameConfig
from flappy_bird_demo.pipe import Pipe, make_pipe


@pytest.fixture
def config() -> GameConfig:
    return GameConfig()


@pytest.fixture
def pipe(config: GameConfig) -> Pipe:
    # gap_y=200 means top pipe covers 0..200, gap covers 200..350, bottom pipe 350..600
    return Pipe(x=300.0, gap_y=200, width=config.pipe_width, gap=config.pipe_gap)


def test_pipe_moves_left(pipe: Pipe, config: GameConfig) -> None:
    initial_x = pipe.x
    pipe.move(config)
    assert pipe.x == initial_x - config.pipe_speed


def test_pipe_off_screen(config: GameConfig) -> None:
    pipe = Pipe(x=-(config.pipe_width + 1), gap_y=200, width=config.pipe_width, gap=config.pipe_gap)
    assert pipe.is_off_screen() is True


def test_pipe_not_off_screen(pipe: Pipe) -> None:
    assert pipe.is_off_screen() is False


def test_pipe_collision_inside_gap(pipe: Pipe) -> None:
    # Bird rect sits entirely within the gap (y=210, height=24 → bottom at 234, gap ends at 350)
    bird_rect = (pipe.x + 1, 210, 34, 24)
    assert pipe.collides_with(bird_rect) is False


def test_pipe_collision_top_section(pipe: Pipe) -> None:
    # Bird rect overlaps the top pipe section (gap_y=200, bird y=180 → top of gap)
    bird_rect = (pipe.x + 1, 180, 34, 24)
    assert pipe.collides_with(bird_rect) is True


def test_pipe_collision_bottom_section(pipe: Pipe) -> None:
    # Bottom pipe starts at gap_y + gap = 350; bird y=340, height=24 → bottom at 364, inside bottom pipe
    bird_rect = (pipe.x + 1, 340, 34, 24)
    assert pipe.collides_with(bird_rect) is True


def test_pipe_passed_by(pipe: Pipe) -> None:
    # Bird rect starts to the right of pipe's right edge
    bird_rect = (int(pipe.x + pipe.width + 1), 200, 34, 24)
    assert pipe.passed_by(bird_rect) is True


def test_make_pipe_returns_pipe_at_screen_width(config: GameConfig) -> None:
    p = make_pipe(config, config.screen_width)
    assert p.x == config.screen_width
    assert p.width == config.pipe_width
    assert p.gap == config.pipe_gap
