"""Game state logic — no pygame dependency."""

from enum import Enum, auto

from flappy_bird_demo.bird import Bird
from flappy_bird_demo.config import GameConfig
from flappy_bird_demo.pipe import Pipe, make_pipe
from flappy_bird_demo.score import Score


class GameState(Enum):
    IDLE = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.bird = Bird(
            x=float(config.bird_x),
            y=float(config.screen_height // 2),
            width=config.bird_width,
            height=config.bird_height,
        )
        self.score = Score()
        self.pipes: list[Pipe] = []
        self.state = GameState.IDLE
        self.tick_count: int = 0
        self._counted_pipe_ids: set[int] = set()

    def handle_flap(self) -> None:
        """Respond to a flap input depending on current state."""
        if self.state == GameState.IDLE:
            self.state = GameState.PLAYING
            self.bird.flap(self.config)
        elif self.state == GameState.PLAYING:
            self.bird.flap(self.config)

    def update(self) -> None:
        """Advance the simulation by one tick (only when PLAYING)."""
        if self.state != GameState.PLAYING:
            return

        self.bird.update(self.config)

        # Spawn a new pipe at the configured interval (fires at tick 0, 90, 180, ...)
        if self.tick_count % self.config.pipe_spawn_interval == 0:
            self.pipes.append(make_pipe(self.config, self.config.screen_width))

        self.tick_count += 1

        bird_rect = self.bird.rect

        # Move pipes and remove those that have left the screen
        active: list[Pipe] = []
        for pipe in self.pipes:
            pipe.move(self.config)
            if not pipe.is_off_screen():
                active.append(pipe)
            else:
                # Clean up tracking set to avoid unbounded growth
                self._counted_pipe_ids.discard(id(pipe))
        self.pipes = active

        # Score and collision checks
        for pipe in self.pipes:
            pipe_id = id(pipe)
            if pipe.passed_by(bird_rect) and pipe_id not in self._counted_pipe_ids:
                self.score.increment()
                self._counted_pipe_ids.add(pipe_id)
            if pipe.collides_with(bird_rect):
                self.state = GameState.GAME_OVER
                return

        if self.bird.is_out_of_bounds(self.config):
            self.state = GameState.GAME_OVER

    def reset(self) -> None:
        """Reset for a new game while preserving the high score."""
        self.score.reset()
        self.bird = Bird(
            x=float(self.config.bird_x),
            y=float(self.config.screen_height // 2),
            width=self.config.bird_width,
            height=self.config.bird_height,
        )
        self.pipes = []
        self.tick_count = 0
        self._counted_pipe_ids = set()
        self.state = GameState.IDLE
