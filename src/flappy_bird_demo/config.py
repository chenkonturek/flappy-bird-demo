"""Game configuration constants."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """Immutable configuration for all game constants."""

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
