"""Integration tests for flappy_bird_demo."""

import os

import pytest

from flappy_bird_demo.config import GameConfig
from flappy_bird_demo.game import Game, GameState


@pytest.fixture
def config() -> GameConfig:
    return GameConfig()


@pytest.fixture
def game(config: GameConfig) -> Game:
    return Game(config)


def test_full_game_tick_sequence(game: Game) -> None:
    """Bird falls with no flaps; game must reach GAME_OVER within 2000 ticks."""
    game.handle_flap()  # IDLE → PLAYING (one flap to start; no further input)
    for _ in range(2000):
        if game.state == GameState.GAME_OVER:
            break
        game.update()
    assert game.state == GameState.GAME_OVER


def test_game_survives_many_flaps(game: Game) -> None:
    """Rapid flap + update calls must not crash and must stay in a valid GameState."""
    valid_states = set(GameState)
    for _ in range(500):
        game.handle_flap()
        game.update()
    assert game.state in valid_states


# ---------------------------------------------------------------------------
# Renderer / InputHandler tests — skipped in CI (need a display)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="needs display")
class TestRenderer:
    """Placeholder for renderer / input-handler tests that require a display."""

    def test_renderer_placeholder(self) -> None:
        """Renderer tests go here once pygame is available."""
        pass
