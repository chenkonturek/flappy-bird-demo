"""Pygame rendering — the only module that imports pygame."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flappy_bird_demo.game import Game

from flappy_bird_demo.config import GameConfig
from flappy_bird_demo.game import GameState


class Renderer:  # pragma: no cover
    def __init__(self, config: GameConfig) -> None:
        import pygame  # noqa: PLC0415

        self._pygame = pygame
        self.config = config
        pygame.init()
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

    def draw_frame(self, game: "Game") -> None:  # pragma: no cover
        pygame = self._pygame
        config = self.config

        # Background
        self.screen.fill((135, 206, 235))  # Sky blue

        # Pipes
        for pipe in game.pipes:
            px = int(pipe.x)
            # Top pipe
            pygame.draw.rect(self.screen, (34, 139, 34), (px, 0, pipe.width, pipe.gap_y))
            # Bottom pipe
            bottom_y = pipe.gap_y + pipe.gap
            pygame.draw.rect(
                self.screen,
                (34, 139, 34),
                (px, bottom_y, pipe.width, config.screen_height - bottom_y),
            )

        # Bird
        bx, by, bw, bh = game.bird.rect
        pygame.draw.rect(self.screen, (255, 215, 0), (bx, by, bw, bh))  # Yellow

        # Score
        score_surf = self.font.render(str(game.score.current), True, (255, 255, 255))
        self.screen.blit(score_surf, (config.screen_width // 2 - score_surf.get_width() // 2, 20))

        # State overlays
        if game.state == GameState.IDLE:
            msg = self.small_font.render("Press SPACE / click to start", True, (255, 255, 255))
            self.screen.blit(msg, (config.screen_width // 2 - msg.get_width() // 2, config.screen_height // 2 + 40))
        elif game.state == GameState.GAME_OVER:
            over_surf = self.font.render("GAME OVER", True, (220, 50, 50))
            self.screen.blit(
                over_surf, (config.screen_width // 2 - over_surf.get_width() // 2, config.screen_height // 2 - 30)
            )
            hi_surf = self.small_font.render(f"Best: {game.score.high}", True, (255, 255, 255))
            self.screen.blit(
                hi_surf, (config.screen_width // 2 - hi_surf.get_width() // 2, config.screen_height // 2 + 10)
            )
            restart_surf = self.small_font.render("Press SPACE / click to restart", True, (255, 255, 255))
            self.screen.blit(
                restart_surf,
                (config.screen_width // 2 - restart_surf.get_width() // 2, config.screen_height // 2 + 40),
            )

        pygame.display.flip()

    def tick(self, fps: int) -> None:  # pragma: no cover
        self.clock.tick(fps)

    def close(self) -> None:  # pragma: no cover
        self._pygame.quit()
