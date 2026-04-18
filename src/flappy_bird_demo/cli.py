"""Console script for flappy_bird_demo."""

import typer

from flappy_bird_demo.config import GameConfig
from flappy_bird_demo.game import Game, GameState
from flappy_bird_demo.input_handler import InputHandler
from flappy_bird_demo.renderer import Renderer

app = typer.Typer()


@app.command()
def main() -> None:
    """Launch the Flappy Bird game."""
    config = GameConfig()
    game = Game(config)
    renderer = Renderer(config)
    handler = InputHandler()
    try:
        while True:
            flap, quit_ = handler.poll()
            if quit_:
                break
            if flap:
                if game.state == GameState.GAME_OVER:
                    game.reset()
                else:
                    game.handle_flap()
            game.update()
            renderer.draw_frame(game)
            renderer.tick(config.fps)
    finally:
        renderer.close()


if __name__ == "__main__":
    app()
