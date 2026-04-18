# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tooling

This project is managed with **uv** and **just**. All Python commands run under `uv run`, which resolves the `dev` dependency group by default (`pyproject.toml` sets `[tool.uv] default-groups = ["dev"]`). The `justfile` pins `--python=3.14` for local work even though the supported range is 3.12–3.14.

## Common commands

- `just qa` — full local gate: `ruff format`, `ruff check --fix`, isort via `ruff --select I --fix`, `ty check`, `pytest`. Run this before committing.
- `just test` / `just t` — run pytest on 3.14. Forwards args, e.g. `just test tests/test_flappy_bird_demo.py::test_import -k pattern -x`.
- `just testall` — pytest on 3.12, 3.13, 3.14 (mirrors CI's matrix).
- `just pdb ARGS` — pytest with `--pdb --maxfail=10`.
- `just coverage` — runs `coverage run -m pytest` on each Python, then `coverage combine` + `report` + `html`. Coverage is configured branch+parallel, `fail_under = 50`, sources `src/` and `tests/`.
- `just type-check` / `tc` — `ty check .` (also `type-check-concise`, `type-check-watch`).
- `just docs-serve` / `d` — kills anything on :8000 then runs `zensical serve` (docs group). `just docs-build` does a clean build.
- `just build` / `b` — wipes `build/` and `dist/`, then `uv build`.
- `just clean` / `c` — removes build, pyc, and test/coverage artifacts.

CI (`.github/workflows/ci.yml`) runs lint, `ty check`, the 3.12/3.13/3.14 test matrix, and a coverage-combine job gated by `all-checks-pass`. Keep `just qa` green to match CI.

## Code layout

- `src/flappy_bird_demo/` — the installable package (src-layout, `py.typed` shipped).
  - `cli.py` exposes `app = typer.Typer()` with a single `main` command; rendering uses `rich.console.Console`. `pyproject.toml` wires `flappy_bird_demo = "flappy_bird_demo.cli:app"` as the console script, and `__main__.py` re-exports `app` so `python -m flappy_bird_demo` works too.
  - `utils.py` holds helpers invoked from the CLI.
- `tests/` — pytest suite (`testpaths = ["tests"]`).
- `scripts/release.py` — standalone PEP 723 script; reads `pyproject.toml` and `CHANGELOG/<version>.md`, then runs `git tag -a v<version>`, `git push origin <tag>`, and `gh release create`.
- `docs/` — Zensical site (`zensical.toml` at the root). API reference is auto-generated via `mkdocstrings-python`, so add real docstrings when adding public API.
- `CHANGELOG/<version>.md` — per-release notes file consumed by `scripts/release.py`; the first `# ` line becomes the release title.

## Release flow

1. Bump with `uv version <version>` (or `--bump minor`) and write `CHANGELOG/<version>.md`.
2. Commit `pyproject.toml`, `uv.lock`, and the changelog entry with message `Release <version>`.
3. `just release` — tags, pushes, creates the GitHub Release. The tag push triggers `.github/workflows/publish.yml`, which builds, generates SLSA provenance, and publishes to PyPI via trusted publishing. `just publish` is the manual fallback (`uv build && uv publish`).

## Conventions enforced by config

- Ruff: line length 120; lint rules `E, W, F, I, B, UP`. `ruff format` is the formatter — do not hand-format.
- Type checking via `ty` (Astral). All rules default to error; override in `[tool.ty]` only when necessary.
- Python floor is 3.12 (`requires-python = ">= 3.12"`); avoid syntax or stdlib usage that breaks on 3.12.