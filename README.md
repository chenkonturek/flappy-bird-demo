# flappy-bird-demo

![PyPI version](https://img.shields.io/pypi/v/flappy-bird-demo.svg)

A terminal-playable Flappy Bird game implemented in Python using pygame-ce. Control a bird through procedurally-generated pipes and beat your high score.

* [GitHub](https://github.com/chenkonturek/flappy-bird-demo/) | [PyPI](https://pypi.org/project/flappy-bird-demo/) | [Documentation](https://chenkonturek.github.io/flappy-bird-demo/)
* Created by [Chen Konturek](https://github.com/chenkonturek/)
* MIT License

## Features

* pygame-ce powered 2D game running at 60 FPS in a 400×600 window
* Physics simulation with gravity and flap mechanics
* Procedurally generated pipes with randomised gaps
* Session score + all-time high score tracking
* Clean architecture: game logic fully separated from rendering and input

## Controls

| Key / Action | Effect |
|---|---|
| Space / Mouse click | Flap / Start / Restart |
| Esc / Close window | Quit |

## Quickstart

```bash
pip install flappy-bird-demo
flappy_bird_demo
```

Or run from source:

```bash
uv tool install --editable .
flappy_bird_demo
```

## Author

flappy-bird-demo was created in 2026 by Chen Konturek.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
