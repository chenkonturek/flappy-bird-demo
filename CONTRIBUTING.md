# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/chenkonturek/flappy-bird-demo/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

flappy-bird-demo could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

To preview the docs locally:

```sh
just docs-serve
```

This starts a local server at http://localhost:8000 with live reload. Edit files in `docs/` or add docstrings to your code (the API reference page is auto-generated via `mkdocstrings-python`).

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/chenkonturek/flappy-bird-demo/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up flappy-bird-demo for local development.

1. Fork the flappy-bird-demo repo on GitHub.
2. Clone your fork locally:

   ```sh
   git clone git@github.com:chenkonturek/flappy-bird-demo.git
   ```

3. Install your local copy with uv:

   ```sh
   cd flappy-bird-demo/
   uv sync
   ```

4. Create a branch for local development:

   ```sh
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass linting, type checking, and the tests:

   ```sh
   just qa
   ```

   This runs `ruff format`, `ruff check --fix`, isort, `ty check`, and `pytest`. Or run the tests alone:

   ```sh
   just test
   ```

6. Commit your changes and push your branch to GitHub:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring (Google Python Style), and add the feature to the list in README.md.
3. The pull request should work for Python 3.12, 3.13, and 3.14. Tests run in GitHub Actions on every pull request to the main branch — make sure the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```sh
just test tests/test_flappy_bird_demo.py::test_name
```

Or pass pytest flags directly:

```sh
just test -k pattern -x
```

To run tests across all supported Python versions:

```sh
just testall
```

To run tests with coverage:

```sh
just coverage
```

To run type checking:

```sh
just type-check
```

## Releasing a New Version

1. **Bump the version** and **write the changelog:**
   ```bash
   uv version <version>        # or: uv version --bump minor
   ```
   Then write `CHANGELOG/<version>.md`. See previous entries for the format.
2. **Commit:**
   ```bash
   git add pyproject.toml uv.lock CHANGELOG/
   git commit -m "Release <version>"
   ```
3. **Release:**
   ```bash
   just release
   ```
   This creates an annotated `v*` tag, pushes it to GitHub, and creates a
   GitHub Release with the changelog contents as release notes. The tag
   push triggers `.github/workflows/publish.yml`, which builds the package,
   generates SLSA provenance attestations, and publishes to PyPI via
   trusted publishing.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
