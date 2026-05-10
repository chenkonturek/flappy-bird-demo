# Capability: CLI and Input Handling

The CLI layer consists of `cli.py` (the Typer application and game loop) and `input_handler.py` (the pygame event translator). Together they form the entry point that wires user input to game logic and drives the frame loop.

---

### Requirement: The package exposes a `flappy_bird_demo` console script
`pyproject.toml` registers `flappy_bird_demo = "flappy_bird_demo.cli:app"` as a console script. After installation, running `flappy_bird_demo` in any shell launches the game.

#### Scenario: Console script entry point is wired correctly
- **WHEN** the package is installed
- **THEN** `flappy_bird_demo` is available as a command that invokes `cli.app`

---

### Requirement: The package is runnable as a Python module
`__main__.py` re-exports `app` so that `python -m flappy_bird_demo` works without installation.

#### Scenario: Module invocation works
- **WHEN** `python -m flappy_bird_demo` is run
- **THEN** the same `main()` command executes as via the console script

---

### Requirement: The main command initialises all subsystems from a shared config
`main()` constructs `GameConfig`, `Game(config)`, `Renderer(config)`, and `InputHandler()` before entering the game loop. All subsystems share the same `GameConfig` instance.

#### Scenario: Subsystems constructed from one config
- **WHEN** `main()` is called
- **THEN** `Game`, `Renderer`, and `InputHandler` are all initialised before the loop begins

---

### Requirement: The game loop polls input, updates state, and renders on every frame
Each iteration of the loop follows this fixed order:
1. `handler.poll()` → `(flap, quit_)`
2. If `quit_` is `True`, break out of the loop.
3. If `flap` is `True` and `game.state == GAME_OVER`, call `game.reset()`.
4. Else if `flap` is `True`, call `game.handle_flap()`.
5. `game.update()`
6. `renderer.draw_frame(game)`
7. `renderer.tick(config.fps)`

#### Scenario: Loop processes one frame per iteration
- **WHEN** the game loop runs
- **THEN** poll → update → draw → tick happen in that order every iteration

---

### Requirement: Space bar triggers a flap action
`InputHandler.poll()` returns `flap=True` when a `KEYDOWN` event for `pygame.K_SPACE` is in the event queue.

#### Scenario: Space key produces flap signal
- **WHEN** the Space key is pressed
- **THEN** `poll()` returns `(True, False)`

---

### Requirement: Left mouse button click triggers a flap action
`InputHandler.poll()` returns `flap=True` when a `MOUSEBUTTONDOWN` event with `button == 1` is in the event queue.

#### Scenario: Left click produces flap signal
- **WHEN** the left mouse button is clicked
- **THEN** `poll()` returns `(True, False)`

---

### Requirement: Escape key triggers quit
`InputHandler.poll()` returns `quit=True` when a `KEYDOWN` event for `pygame.K_ESCAPE` is in the event queue.

#### Scenario: Escape key produces quit signal
- **WHEN** the Escape key is pressed
- **THEN** `poll()` returns `(False, True)`

---

### Requirement: Window close button triggers quit
`InputHandler.poll()` returns `quit=True` when a `pygame.QUIT` event (e.g. the OS window close button) is in the event queue.

#### Scenario: Window close produces quit signal
- **WHEN** the window close button is clicked
- **THEN** `poll()` returns `(False, True)`

---

### Requirement: Multiple events in one frame are all processed
`InputHandler.poll()` iterates the full pygame event queue. If both a flap event and a quit event arrive in the same frame, `flap=True` and `quit=True` are both returned.

#### Scenario: Simultaneous flap and quit events both register
- **WHEN** both a Space key press and a window-close event are in the queue
- **THEN** `poll()` returns `(True, True)`

---

### Requirement: Flap during GAME_OVER triggers a reset rather than a flap
The CLI distinguishes GAME_OVER: if `flap=True` and `game.state == GAME_OVER`, it calls `game.reset()` instead of `game.handle_flap()`.

#### Scenario: Flap on game-over resets the game
- **WHEN** `game.state == GAME_OVER` and `flap=True`
- **THEN** `game.reset()` is called, state returns to IDLE

---

### Requirement: renderer.close() is always called on exit
`main()` wraps the game loop in a `try/finally` block. `renderer.close()` is called in the `finally` clause, ensuring pygame shuts down cleanly whether the loop exits normally or via an exception.

#### Scenario: Renderer is closed after the loop
- **WHEN** the game loop exits for any reason
- **THEN** `renderer.close()` is called exactly once
