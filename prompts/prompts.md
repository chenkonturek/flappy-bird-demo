# Prompts for Flappy Bird Project

---

## 1. Project Initialisation

Install cookiecutter if not already present. Create a project folder called `flappy-bird-demo` and initialise it with the `cookiecutter-pypackage` template.

Commit the changes and push to GitHub: https://github.com/chenkonturek

---

## 2. Game Design & Planning

We'd like to create a Flappy Bird game in Python with good graphics. Follow Python coding best practices and use a modular design. Prepare a testing plan.

---

## 3. Implementation (Parallel Subagents)

Create two subagents:
- Based on `@specs/specs.md`, use one subagent to write the code.
- Use a second subagent to write the tests.

---

## 4. Bird Graphic Enhancement

Enhance the bird graphic to make it look more like a real bird. Update both code and tests accordingly.

Create a new branch, commit the changes, and raise a PR.

---

## 5. Sync Main Branch

```
git checkout main && git pull
```

---

## 6. Coding Standards

Enhance the project-level `CLAUDE.md` to define better Python coding standards.

Create a new branch, commit the changes, and raise a PR.

---

## 7. Sync Main Branch

```
git checkout main && git pull
```

---

## 8. Code Refactor

Refactor the code based on the coding standards specified in `@CLAUDE.md`.

Create a new branch, commit the changes, and raise a PR.

---

## 9. Sync Main Branch

```
git checkout main && git pull
```

---

## 10. README Updates

Update the content in `@README.md`.

Create a new branch, commit the changes, and raise a PR. Then apply the following incremental improvements:

- Remove the Development and Documentation sections.
- Update the QuickStart section to install from the GitHub repo with installation and run instructions.
- Update the PR description.
- Remove PyPI and Documentation references from the intro.
- Add `@docs/images/icon.png` to the README.
- Add Python version and unit tests passed badges.
- Remove the PyPI version badge.
- Commit changes and raise a PR; update the PR description.
- Make the icon image smaller and position it below the description.

---

## 11. Sync Main Branch

```
git checkout main && git pull
```

---

## 12. Docstring Enhancement

Update `@CLAUDE.md` to refine docstring standards: include input/output descriptions and class descriptions using Google Python Style.

Enhance docstrings in `@src` based on `@README.md`.

Create a new branch, commit, and push. Then:

- Update the `just test` command in `@CLAUDE.md` to use Python 3.12.
- Update the Python version in `@README.md` based on `testall` in `@CLAUDE.md`.
- Commit, push, and raise a PR.
- Generate API docs from docstrings.

---

## 13. Changelog & Release Prep

Update `@CHANGELOG/0.1.0.md` and remove the PyPI deployment step.

Create a release branch and raise a PR.

Redo the release from `main` without PyPI deployment.

---

## 14. GitHub Release

Create a GitHub release using the `main` branch for version `0.1.0`.
