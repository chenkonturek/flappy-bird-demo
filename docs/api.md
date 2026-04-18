# API Reference

## Configuration

::: flappy_bird_demo.config
    options:
      members:
        - GameConfig

## Game entities

::: flappy_bird_demo.bird
    options:
      members:
        - Bird

::: flappy_bird_demo.pipe
    options:
      members:
        - Pipe
        - make_pipe

::: flappy_bird_demo.score
    options:
      members:
        - Score

## Game logic

::: flappy_bird_demo.game
    options:
      members:
        - GameState
        - Game

## Input & rendering

::: flappy_bird_demo.input_handler
    options:
      members:
        - InputHandler

::: flappy_bird_demo.renderer
    options:
      members:
        - Renderer

## CLI

::: flappy_bird_demo.cli
    options:
      members:
        - main
