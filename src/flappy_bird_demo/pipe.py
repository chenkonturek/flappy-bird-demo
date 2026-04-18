"""Pipe entity — no pygame dependency."""

import random
from dataclasses import dataclass

from flappy_bird_demo.config import GameConfig


@dataclass
class Pipe:
    x: float
    gap_y: int
    width: int
    gap: int

    def move(self, config: GameConfig) -> None:
        """Advance the pipe toward the left edge."""
        self.x -= config.pipe_speed

    def is_off_screen(self) -> bool:
        """Return True when the pipe has scrolled completely off screen."""
        return self.x + self.width < 0

    def collides_with(self, bird_rect: tuple[float, int, int, int]) -> bool:
        """Return True if the bird overlaps this pipe's top or bottom segment."""
        bx, by, bw, bh = bird_rect
        # Horizontal overlap check (same for both segments)
        if bx + bw <= self.x or bx >= self.x + self.width:
            return False
        # Top pipe segment: y=0 to y=gap_y
        if by < self.gap_y:
            return True
        # Bottom pipe segment: y=gap_y+gap to y=infinity
        if by + bh > self.gap_y + self.gap:
            return True
        return False

    def passed_by(self, bird_rect: tuple[float, int, int, int]) -> bool:
        """Return True when the bird's leading edge has cleared the pipe."""
        return self.x + self.width < bird_rect[0]


def make_pipe(config: GameConfig, screen_width: int) -> Pipe:
    """Create a new pipe entering from the right side of the screen."""
    gap_y = random.randint(80, config.screen_height - config.pipe_gap - 80)
    return Pipe(x=float(screen_width), gap_y=gap_y, width=config.pipe_width, gap=config.pipe_gap)
