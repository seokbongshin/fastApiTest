# AGENTS.md

## Project Overview

This project is a Python 3.12 backend service using FastAPI.

The main purpose of this project is:

- Build REST APIs with FastAPI.
- Execute internal Python logic, functions, scripts, or processing modules.
- Return the processed Python results through HTTP API responses.
- Keep the implementation simple, explicit, and easy to maintain.

This project is not intended to be a large enterprise framework or over-engineered platform unless explicitly requested.

---

## Environment

- Python version: 3.12
- Main web framework: FastAPI
- ASGI server: Uvicorn
- Dependency management: pip and requirements.txt by default

Do not downgrade or upgrade the Python version unless explicitly requested.

---

## Recommended Project Structure

Prefer the following structure unless the existing project already has a different structure:

```text
project-root/
├── AGENTS.md
├── README.md
├── requirements.txt
├── .env
├── .gitignore
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   └── routes.py
    ├── core/
    │   ├── __init__.py
    │   └── config.py
    ├── services/
    │   ├── __init__.py
    │   └── processing_service.py
    ├── schemas/
    │   ├── __init__.py
    │   └── response_schema.py
    └── utils/
        ├── __init__.py
        └── helpers.py
```

---

## Build and Run Commands

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment on Windows

```bash
.venv\Scripts\activate
```

### Activate virtual environment on Linux or macOS or windows

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run development server

```bash
uvicorn app.main:app --reload
```

### Run with explicit host and port

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## FastAPI Rules

- Define the FastAPI application in `app/main.py`.
- Keep route handlers thin.
- Route handlers should call service functions instead of containing business logic directly.
- Use Pydantic models for request and response schemas when the API input/output becomes non-trivial.
- Return JSON-compatible objects only.
- Use clear HTTP status codes.
- Add `/health` endpoint for basic health checks.

Example:

```python
from fastapi import FastAPI

app = FastAPI(title="Python Result API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

## Service Layer Rules

Internal Python processing logic should be placed under `app/services`.

Route handlers should call service functions.

Good:

```python
@app.post("/process")
def process(request: ProcessRequest):
    result = processing_service.run(request.input)
    return {"result": result}
```

Bad:

```python
@app.post("/process")
def process(request: ProcessRequest):
    # Do not put complex processing logic directly in the route.
    ...
```

---

## Python Coding Rules

- Use Python 3.12 syntax.
- Prefer simple, readable code over clever code.
- Use type hints for function parameters and return values.
- Use meaningful function and variable names.
- Keep functions small and focused.
- Avoid unnecessary abstraction.
- Avoid global mutable state.
- Do not hide exceptions silently.
- Use standard library features when possible before adding new dependencies.

---

## Error Handling Rules

- Raise `HTTPException` in API layer for expected API errors.
- Catch and convert known service errors into clear API responses.
- Do not expose sensitive internal exception details to API clients.
- Log unexpected exceptions where appropriate.

Example:

```python
from fastapi import HTTPException

if not input_value:
    raise HTTPException(status_code=400, detail="input_value is required")
```

---

## Configuration Rules

- Use `.env` for local environment variables.
- Do not hardcode secrets, API keys, database passwords, or private URLs.
- Load environment variables in a central config module such as `app/core/config.py`.
- Keep default values safe for local development.

Recommended dependencies:

```text
python-dotenv
pydantic
pydantic-settings
```

---

## Dependency Rules

Default `requirements.txt` may include:

```text
fastapi
uvicorn[standard]
python-dotenv
pydantic
pydantic-settings
```

Only add new dependencies when they are clearly needed.

Before adding a dependency, check whether the same goal can be achieved cleanly with the Python standard library.

---

## API Response Rules

Prefer consistent API responses.

Example success response:

```json
{
  "success": true,
  "data": {},
  "message": null
}
```

Example error response:

```json
{
  "success": false,
  "data": null,
  "message": "Invalid request"
}
```

If the project already has a different response format, follow the existing format.

---

## Logging Rules

- Use Python `logging`.
- Do not use excessive `print()` statements in production code.
- Logs should help debugging without exposing secrets.
- Log key processing steps for long-running or important internal Python jobs.

---

## Testing Rules

- Use `pytest` when tests are needed.
- Prefer testing service functions first.
- Use FastAPI `TestClient` for API tests.
- Do not require external services for simple unit tests.

Recommended test structure:

```text
tests/
├── test_health.py
└── test_processing_service.py
```

---

## Forbidden Patterns

Do not do the following unless explicitly requested:

- Do not downgrade Python below 3.12.
- Do not introduce Django, Flask, Spring, Node.js, or other frameworks.
- Do not put heavy business logic directly inside FastAPI route handlers.
- Do not hardcode secrets.
- Do not create unnecessary classes for simple functions.
- Do not introduce async code unless it provides real benefit.
- Do not use global variables to store request-specific data.
- Do not add database, queue, cache, or scheduler dependencies unless requested.
- Do not over-engineer the project structure.

---

## Preferred Patterns

Prefer this style:

```python
def calculate_result(input_value: str) -> dict:
    return {
        "input": input_value,
        "length": len(input_value),
    }
```

Prefer this API style:

```python
from fastapi import APIRouter
from app.services.processing_service import calculate_result

router = APIRouter()

@router.post("/process")
def process(input_value: str):
    result = calculate_result(input_value)
    return {
        "success": True,
        "data": result,
        "message": None,
    }
```

---

## Agent Behavior Rules

When working on this project:

- First inspect existing files and follow the current structure.
- Make the smallest safe change.
- Preserve existing behavior unless the user asks for a change.
- Explain important design decisions briefly.
- Prefer simple working code over theoretical architecture.
- When adding a new API, include an example request and response if useful.
- When adding dependencies, update `requirements.txt`.
- When changing run behavior, update `README.md` if it exists.
- Avoid large refactoring unless explicitly requested.
