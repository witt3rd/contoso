# Contoso FastAPI Service

A simple FastAPI service.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1. **Install uv:**
   Follow the instructions on the [uv installation guide](https://github.com/astral-sh/uv#installation).

2. **Create a virtual environment:**

   ```bash
   uv venv
   ```

3. **Activate the virtual environment:**

   - On macOS and Linux:

     ```bash
     source .venv/bin/activate
     ```

   - On Windows (PowerShell):

     ```powershell
     .venv\Scripts\Activate.ps1
     ```

4. **Install dependencies:**

   ```bash
   uv pip install -e .[dev]
   ```

   (Assuming you might add a `dev` extra for development tools later in `pyproject.toml`)
   If you don't have/want a `dev` extra yet, just use:

   ```bash
   uv pip install -e .
   ```

## Running the service

To run the FastAPI service locally:

```bash
uvicorn src.contoso.index:app --reload
```

The service will be available at `http://127.0.0.1:8000`.
