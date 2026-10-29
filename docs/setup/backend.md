# Backend setup

The backend will use Python, FastAPI, and uv. uv will manage the project's
Python version, virtual environment, dependencies, and locked dependency
versions, so contributors do not need to manage a project environment with
`pip` and `venv` separately.

> **Current status:** The backend application and `pyproject.toml` have not
> been scaffolded yet. You can install and verify uv now. The project commands
> later in this guide will work after the backend foundation is added.

## Prerequisites

- Git and a local clone of this repository.
- Docker with Docker Compose.
- The local PostgreSQL service described in [postgresql.md](postgresql.md).
- uv.

The supported Python version will be declared by the backend's
`pyproject.toml` and `.python-version`. Do not select a different project
version independently. uv can install the required Python version when the
backend is initialized.

## Install uv

Choose one installation method.

### Windows

Using WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Or use uv's official installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS and Linux

Using uv's official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Homebrew users may instead run:

```bash
brew install uv
```

Open a new terminal and verify the installation:

```text
uv --version
```

Review downloaded installation scripts before running them if required by your
organization's security policy. See the [official uv installation guide][uv-install]
for other supported installation methods.

## Backend commands after scaffolding

When `backend/pyproject.toml` and the FastAPI application exist, run these
commands from the repository root.

Install the declared Python version and synchronize dependencies:

```text
cd backend
uv sync
```

Run the development API:

```text
uv run fastapi dev app/main.py
```

Run backend tests:

```text
uv run pytest
```

Apply database migrations:

```text
uv run alembic upgrade head
```

The exact commands may be refined when the backend is scaffolded. At that
point, this guide should be updated and every command should be verified on a
fresh development environment.

## Dependency rules

- Add runtime dependencies with `uv add <package>`.
- Add development dependencies with `uv add --dev <package>`.
- Commit both `pyproject.toml` and `uv.lock`.
- Do not commit `.venv/`; it is machine-specific and ignored by Git.
- Run project commands through `uv run` so they use the managed environment.
- Do not place database passwords, AWS credentials, or API keys in source code.

[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
