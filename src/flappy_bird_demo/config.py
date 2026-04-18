"""Game configuration constants."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """Immutable configuration for all game constants.

    Attributes:
        screen_width: Window width in pixels.
        screen_height: Window height in pixels.
        gravity: Downward acceleration applied to the bird each tick.
        flap_strength: Upward velocity applied on each flap input.
        pipe_speed: Pixels each pipe moves left per tick.
        pipe_gap: Height of the passable opening in each pipe pair, in pixels.
        pipe_width: Width of each pipe in pixels.
        pipe_spawn_interval: Ticks between consecutive pipe spawns.
        bird_x: Fixed horizontal position of the bird in pixels.
        bird_width: Bird sprite width in pixels.
        bird_height: Bird sprite height in pixels.
        fps: Target frames per second for the game loop.
    """

    screen_width: int = 400
    screen_height: int = 600
    gravity: float = 0.5
    flap_strength: float = 8.0
    pipe_speed: float = 3.0
    pipe_gap: int = 150
    pipe_width: int = 60
    pipe_spawn_interval: int = 90
    bird_x: int = 80
    bird_width: int = 34
    bird_height: int = 24
    fps: int = 60
