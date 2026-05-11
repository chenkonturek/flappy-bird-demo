"""Console script for flappy_bird_demo."""

import typer

from flappy_bird_demo.audio import SoundManager
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
    audio = SoundManager(config)
    try:
        while True:
            flap, quit_ = handler.poll()
            if quit_:
                break
            prev_score = game.score.current
            prev_state = game.state
            if flap:
                if game.state == GameState.GAME_OVER:
                    game.reset()
                    audio.start_music()
                else:
                    game.handle_flap()
                    audio.play_flap()
            game.update()
            if game.state == GameState.GAME_OVER and prev_state == GameState.PLAYING:
                audio.play_death()
                audio.stop_music()
            if game.score.current > prev_score:
                audio.play_score()
            renderer.draw_frame(game)
            renderer.tick(config.fps)
    finally:
        audio.close()
        renderer.close()


if __name__ == "__main__":
    app()
