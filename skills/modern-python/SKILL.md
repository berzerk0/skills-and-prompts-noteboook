---
name: modern-python
description: Configures Python projects with modern tooling (uv, ruff, ty). Use when creating projects, writing standalone scripts, or migrating from pip/Poetry/mypy/black.
license: CC-BY-SA-4.0
compatibility: [claude, pi, vibe]
---

Guide for modern Python tooling and best practices, based on trailofbits/cookiecutter-python.

## When to Use

- Creating a new Python project or package
- Setting up pyproject.toml configuration
- Configuring development tools (linting, formatting, testing)
- Writing Python scripts with external dependencies

## When NOT to Use

- User wants to keep legacy tooling
- Python < 3.11 required
- Non-Python projects

## Anti-Patterns

| Avoid | Use Instead |
|-------|-------------|
| [tool.ty] python-version | [tool.ty.environment] python-version |
| uv pip install | uv add and uv sync |
| Manual pyproject.toml editing | uv add / uv remove |
| hatchling build backend | uv_build |
| Poetry | uv |
| requirements.txt | PEP 723 for scripts, pyproject.toml for projects |
| mypy / pyright | ty |
| [project.optional-dependencies] | [dependency-groups] (PEP 735) |
| Manual virtualenv activation | uv run |
| pre-commit | prek |

## Key Principles

- Always use uv add and uv remove to manage dependencies
- Never manually activate or manage virtual environments - use uv run
- Use [dependency-groups] for dev/test/docs dependencies
- References loaded on demand, not resident in context
