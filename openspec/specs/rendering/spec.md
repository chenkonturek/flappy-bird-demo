# Capability: Rendering

`Renderer` (in `renderer.py`) is the only module that imports pygame. It owns the pygame window, clock, and fonts. `draw_frame(game)` redraws the entire screen from the current `Game` state on every call. All rendering methods are marked `# pragma: no cover` because they require a live display; they are excluded from CI test coverage.

---

### Requirement: Renderer initialises a pygame window at the configured dimensions
`Renderer.__init__(config)` calls `pygame.init()`, creates a display surface of `(config.screen_width, config.screen_height)`, and sets the caption to `"Flappy Bird"`.

#### Scenario: Window size matches config
- **WHEN** `Renderer(config)` is constructed
- **THEN** the pygame display surface is `config.screen_width × config.screen_height` pixels

#### Scenario: Window caption is set
- **WHEN** `Renderer(config)` is constructed
- **THEN** `pygame.display.get_caption()` returns `"Flappy Bird"`

---

### Requirement: Each frame starts with a sky-blue background
`draw_frame()` fills the entire surface with RGB `(135, 206, 235)` before drawing any other element.

#### Scenario: Background covers the whole surface
- **WHEN** `draw_frame(game)` is called
- **THEN** the surface is filled with `(135, 206, 235)` before pipes or the bird are drawn

---

### Requirement: Pipes are drawn as solid green rectangles
For each `Pipe` in `game.pipes`, `draw_frame()` draws:
- **Top segment**: a rectangle from `(pipe.x, 0)` with width `pipe.width` and height `pipe.gap_y`, filled with RGB `(34, 139, 34)`.
- **Bottom segment**: a rectangle from `(pipe.x, pipe.gap_y + pipe.gap)` with width `pipe.width` extending to the screen floor, filled with RGB `(34, 139, 34)`.

#### Scenario: Both pipe segments are drawn
- **WHEN** `draw_frame(game)` is called with one active pipe
- **THEN** two green rectangles are drawn, one above and one below the gap

---

### Requirement: The bird is drawn as a procedural sprite
`_draw_bird(bx, by, bw, bh)` renders the bird using five pygame primitives, all derived from the bird's bounding box:

| Part | Shape | Colour |
|---|---|---|
| Tail | Left-pointing triangle | `(200, 160, 0)` dark gold |
| Wing | Ellipse at lower body | `(200, 160, 0)` dark gold |
| Body | Ellipse centred on rect | `(255, 215, 0)` gold |
| Head | Circle at the right end | `(255, 225, 50)` bright yellow |
| Eye | Two concentric circles | white `(255,255,255)` / dark `(20,20,20)` |
| Beak | Right-pointing triangle | `(255, 120, 0)` orange |

The sprite is drawn at `(bx, by)` using integer pixel coordinates taken from `bird.rect`.

#### Scenario: Sprite draws without error given valid bounding box
- **WHEN** `_draw_bird(bx, by, bw, bh)` is called with values from `bird.rect`
- **THEN** no exception is raised and the draw calls complete

#### Scenario: Tail geometry is safe with default bird height
- **WHEN** `config.bird_height == 24` (default)
- **THEN** `bh // 2 == 12 >= 5`, so the tail's ±5 px offsets fit within the sprite

---

### Requirement: The current score is displayed at the top centre
`draw_frame()` renders `str(game.score.current)` in white using a 36-point system font, horizontally centred at `screen_width // 2` and vertically at y=20.

#### Scenario: Score label appears at the top centre
- **WHEN** `draw_frame(game)` is called
- **THEN** the score surface is blitted at `x = screen_width // 2 - score_surf.get_width() // 2`, `y = 20`

---

### Requirement: An IDLE overlay prompts the player to start
When `game.state == IDLE`, `draw_frame()` renders `"Press SPACE / click to start"` in white (24-point font) horizontally centred at `screen_height // 2 + 40`.

#### Scenario: Start prompt appears in IDLE state
- **WHEN** `draw_frame(game)` is called with `game.state == IDLE`
- **THEN** the start prompt is blitted at the vertical midpoint + 40

---

### Requirement: A GAME_OVER overlay shows the result and restart prompt
When `game.state == GAME_OVER`, `draw_frame()` renders:
- `"GAME OVER"` in red `(220, 50, 50)` at 36 pt, horizontally centred at `screen_height // 2 - 30`.
- `"Best: <high>"` in white at 24 pt, horizontally centred at `screen_height // 2 + 10`.
- `"Press SPACE / click to restart"` in white at 24 pt, horizontally centred at `screen_height // 2 + 40`.

#### Scenario: Game-over overlay shows all three lines
- **WHEN** `draw_frame(game)` is called with `game.state == GAME_OVER`
- **THEN** "GAME OVER", the best score, and the restart prompt are all rendered

---

### Requirement: tick() caps the frame rate
`Renderer.tick(fps)` calls `self.clock.tick(fps)`, which blocks until enough time has elapsed for the loop to run at no more than `fps` frames per second. The default is `config.fps == 60`.

#### Scenario: tick blocks for the correct duration
- **WHEN** `renderer.tick(60)` is called immediately after `draw_frame()`
- **THEN** the call returns in approximately 1/60 second, capping the loop at 60 FPS

---

### Requirement: close() shuts down pygame
`Renderer.close()` calls `self._pygame.quit()`, releasing the display surface and all pygame resources. It is always called in the `finally` block of `cli.main()`.

#### Scenario: pygame is uninitialised after close
- **WHEN** `renderer.close()` is called
- **THEN** `pygame.get_init()` returns `False`
