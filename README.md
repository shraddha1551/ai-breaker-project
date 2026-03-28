# AI Breaker Project

AI Breaker is a fault injection system that intentionally tests software APIs using invalid inputs.

## Features
- Automated fault injection
- API robustness testing
- Error logging
- Failure detection

## Tech Stack
Python, FastAPI, Uvicorn

## Run the project

### Start server

```bash
python -m uvicorn target_app.app:app --reload