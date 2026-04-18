"""Tests for flappy_bird_demo.game."""

import pytest

from flappy_bird_demo.config import GameConfig
from flappy_bird_demo.game import Game, GameState
from flappy_bird_demo.pipe import Pipe


@pytest.fixture
def config() -> GameConfig:
    return GameConfig()


@pytest.fixture
def game(config: GameConfig) -> Game:
    return Game(config)


def test_game_starts_idle(game: Game) -> None:
    assert game.state == GameState.IDLE


def test_game_starts_on_first_flap(game: Game) -> None:
    game.handle_flap()
    assert game.state == GameState.PLAYING


def test_game_over_on_pipe_collision(game: Game, config: GameConfig) -> None:
    game.handle_flap()  # IDLE → PLAYING
    assert game.state == GameState.PLAYING

    # Place a pipe directly on top of the bird
    bird_rect = game.bird.rect
    colliding_pipe = Pipe(
        x=float(bird_rect[0]),
        gap_y=0,  # gap at very top → bottom pipe covers everything the bird occupies
        width=config.pipe_width,
        gap=1,  # tiny gap so the bird is definitely in the bottom section
    )
    game.pipes = [colliding_pipe]
    game.update()
    assert game.state == GameState.GAME_OVER


def test_game_over_on_ground_hit(game: Game, config: GameConfig) -> None:
    game.handle_flap()  # IDLE → PLAYING
    # Move bird to the ground
    game.bird.y = float(config.screen_height - game.bird.height)
    game.bird.velocity = 0.0
    game.update()
    assert game.state == GameState.GAME_OVER


def test_score_increments_on_pipe_pass(game: Game, config: GameConfig) -> None:
    game.handle_flap()  # IDLE → PLAYING
    assert game.state == GameState.PLAYING

    # Place a pipe that is just behind the bird (already passed) but hasn't been counted
    bird_rect = game.bird.rect
    passed_pipe = Pipe(
        x=float(bird_rect[0] - config.pipe_width - 1),
        gap_y=config.screen_height // 2,
        width=config.pipe_width,
        gap=config.pipe_gap,
    )
    game.pipes = [passed_pipe]
    game.update()
    assert game.score.current > 0


def test_game_resets_on_restart(game: Game) -> None:
    game.handle_flap()  # IDLE → PLAYING
    for _ in range(3):
        game.score.increment()
    game.reset()
    assert game.state == GameState.IDLE
    assert game.score.current == 0


def test_pipes_spawn_over_time(game: Game, config: GameConfig) -> None:
    game.handle_flap()  # IDLE → PLAYING
    ticks_needed = config.pipe_spawn_interval + 1
    for _ in range(ticks_needed):
        if game.state != GameState.PLAYING:
            break
        game.update()
    assert len(game.pipes) > 0
