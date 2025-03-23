# Witty Greeter API

A FastAPI server that responds to GET requests with witty greetings and the provided user's name.

## Installation

```bash
# From the root of the mono-repo
uv sync
```

## Running the Server

```bash
# Using the script entry point with default settings
uv run server

# Specify host and port
uv run server --host 127.0.0.1 --port 9000

# Disable auto-reload
uv run server --no-reload

# Or directly with uvicorn
uvicorn front_end.server:app --reload
```

## Usage

Once the server is running, you can access it at:

- Base URL: http://localhost:8000
- Greeting endpoint: http://localhost:8000/greet/{name}

For example:

- http://localhost:8000/greet/John

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
