"""Bird entity — no pygame dependency."""

from dataclasses import dataclass

from flappy_bird_demo.config import GameConfig


@dataclass
class Bird:
    """Represent the player-controlled bird with physics state.

    Attributes:
        x: Horizontal position in pixels (fixed during play).
        y: Vertical position in pixels; increases downward.
        width: Sprite width in pixels.
        height: Sprite height in pixels.
        velocity: Current vertical speed; negative moves upward.
    """

    x: float
    y: float
    width: int
    height: int
    velocity: float = 0.0

    def flap(self, config: GameConfig) -> None:
        """Apply an upward flap impulse.

        Args:
            config: Game configuration supplying flap_strength.
        """
        self.velocity = -config.flap_strength

    def update(self, config: GameConfig) -> None:
        """Apply gravity and move the bird; clamp at the ceiling.

        Args:
            config: Game configuration supplying gravity and screen_height.
        """
        self.velocity += config.gravity
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0.0

    def is_out_of_bounds(self, config: GameConfig) -> bool:
        """Return True if the bird has fallen below the screen.

        Args:
            config: Game configuration supplying screen_height.

        Returns:
            True when the bird's bottom edge meets or passes the screen floor.
        """
        return self.y + self.height >= config.screen_height

    @property
    def rect(self) -> tuple[int, int, int, int]:
        """Return the bounding box as (x, y, width, height)."""
        return (int(self.x), int(self.y), self.width, self.height)
