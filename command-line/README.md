# Witty Greeter Client

A command-line client that connects to the Witty Greeter API and displays personalized greetings.

## Installation

```bash
# From the root of the mono-repo
uv sync
uv pip install -e command-line
```

## Usage

```bash
# Using the script entry point with default settings
uv run greet John

# Specify host and port
uv run greet John --host 127.0.0.1 --port 9000

# Use a full server URL (overrides host and port)
uv run greet John --server http://other-server:8000

# Or directly using the module
python -m command_line.client John
```

## Arguments

- `name`: Your name (required)
- `--host`: Server hostname or IP (default: localhost)
- `--port`: Server port (default: 8000)
- `--protocol`: Protocol to use (http or https, default: http)
- `--server`, `-s`: Full server URL (overrides host, port, and protocol if provided)

## Examples

```bash
# Get a greeting for the name "Alice"
uv run greet Alice

# Get a greeting from a server on a custom port
uv run greet Bob --port 9000

# Get a greeting from a different host
uv run greet Charlie --host api.example.com
```

## Notes

- Make sure the FastAPI server is running before using this client
- The client will display appropriate error messages if the server is not available
