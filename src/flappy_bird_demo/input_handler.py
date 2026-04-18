"""Pygame input handling — imports pygame."""


class InputHandler:  # pragma: no cover
    """Translate pygame events into flap and quit signals.

    Responds to Space bar and left mouse click (flap), and to Escape and
    window-close events (quit).
    """

    def __init__(self) -> None:
        import pygame  # noqa: PLC0415

        self._pygame = pygame

    def poll(self) -> tuple[bool, bool]:  # pragma: no cover
        """Process the pygame event queue and return (flap, quit) signals.

        Returns:
            A tuple ``(flap, quit)`` where ``flap`` is True when the player
            triggered a flap action and ``quit`` is True when the player
            requested to exit.
        """
        pygame = self._pygame
        flap = False
        quit_ = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_ = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_ = True
                elif event.key == pygame.K_SPACE:
                    flap = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flap = True
        return flap, quit_
