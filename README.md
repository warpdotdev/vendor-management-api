# Vendor Management API

A REST API for tracking and auditing vendor relationships, built with FastAPI and SQLAlchemy.

## Setup

```bash
pip install -e .
```

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

## Project Structure

```
app/
├── main.py          # FastAPI application entry point
├── config.py        # Application settings
├── database.py      # SQLAlchemy engine and session setup
├── models/          # SQLAlchemy ORM models
└── routers/         # API route modules
tests/               # Pytest test suite
```
