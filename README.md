# flappy-bird-demo

![PyPI version](https://img.shields.io/pypi/v/flappy-bird-demo.svg)

Python Boilerplate contains all the boilerplate you need to create a Python package.

* [GitHub](https://github.com/audreyfeldroy/flappy-bird-demo/) | [PyPI](https://pypi.org/project/flappy-bird-demo/) | [Documentation](https://audreyfeldroy.github.io/flappy-bird-demo/)
* Created by [Chen Konturek](https://audrey.feldroy.com/) | GitHub [@audreyfeldroy](https://github.com/audreyfeldroy) | PyPI [@audreyfeldroy](https://pypi.org/user/audreyfeldroy/)
* MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://audreyfeldroy.github.io/flappy-bird-demo/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/flappy-bird-demo.git
cd flappy-bird-demo

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `flappy_bird_demo`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

flappy-bird-demo was created in 2026 by Chen Konturek.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
