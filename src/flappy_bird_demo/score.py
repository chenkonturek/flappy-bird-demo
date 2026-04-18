"""Score tracking — no pygame dependency."""


class Score:
    """Track current and all-time high score.

    Attributes:
        current: Points accumulated in the ongoing session.
        high: Highest score achieved since the process started.
    """

    def __init__(self) -> None:
        self.current: int = 0
        self.high: int = 0

    def increment(self) -> None:
        """Add one point to the current score."""
        self.current += 1

    def reset(self) -> None:
        """Save the high score then zero the current score."""
        self.high = max(self.high, self.current)
        self.current = 0
