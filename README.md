# AI Breaker Project

AI Breaker is a fault injection system that intentionally tests software APIs using invalid inputs.

## Features
- Automated random input testing
- API robustness and failure detection
- Backend error logging and analysis
- Structured JSON output for further processing

## Tech Stack
Python, FastAPI, Uvicorn

## Run the project

### Start server

```bash
python -m uvicorn target_app.app:app --reload
