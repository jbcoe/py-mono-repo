# UV Workspace Demo

This repository demonstrates how to use [uv](https://github.com/astral-sh/uv) to manage multiple Python projects in a single repository (monorepo) using workspace functionality. It showcases best practices for shared dependencies, configuration, and project organization.

## Repository Structure

```ascii
mono-repo-py/
├── pyproject.toml          # Root workspace configuration
├── core/                   # Shared core library
│   ├── pyproject.toml      # Core package configuration
│   └── src/xyz/core/       # Core package source code
├── api/                    # FastAPI server package
│   ├── pyproject.toml      # API package configuration
│   └── src/api/            # API package source code
└── command-line/           # CLI client package
    ├── pyproject.toml      # CLI package configuration
    └── src/command_line/   # CLI package source code
```

## Key Features

- **Workspace Configuration**: Using UV's workspace feature to manage multiple packages
- **Shared Dependencies**: Core package provides shared configuration and utilities
- **Consistent Versioning**: All packages can be versioned and developed together
- **Simplified Development**: Developers can work on multiple packages simultaneously
- **Centralized Logging**: Common logging infrastructure across all packages

## How It Works

### Root Configuration

The root `pyproject.toml` defines the workspace:

```toml
[tool.uv.workspace]
members = [
    "core",
    "command-line",
    "api",
]

[tool.uv.sources]
xyz-core = { workspace = true }
command-line = { workspace = true }
api = { workspace = true }
```

### Package Configuration

Each package has its own `pyproject.toml` that defines:

1. Package metadata and dependencies
2. Build system configuration
3. Entry points (if needed)

Example from the command-line package:

```toml
[project]
name = "xyz-command-line"
version = "0.1.0"
dependencies = [
    "requests>=2.31.0",
    "xyz-core",  # Dependency on another workspace package
]

[project.scripts]
greet = "command_line.client:main"
```

### Shared Code and Configuration

The `core` package provides shared configuration used by both the API and CLI:

```python
# In core/src/xyz/core/config.py
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
GREETING_ENDPOINT = "/greet/{name}"
```

This allows consistent settings across packages:

```python
# In command-line/src/command_line/client.py
from xyz.core import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_PROTOCOL, GREETING_ENDPOINT
```

### Logging Infrastructure

The project includes a centralized logging system in the core package:

```python
# In your application code
from xyz.core import configure_logging, get_logger

# Set up a logger for the current module
logger = get_logger(__name__)

# Configure logging with command line args
configure_logging(level="DEBUG", log_file="app.log")

# Use the logger
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

Both the API server and command-line client support:

- Debug logging with the `--debug` flag
- Writing logs to a file with `--log-file FILENAME`
- Consistent log formatting across all packages

## Getting Started

### Setup

```bash
# Clone the repository
git clone https://github.com/example/mono-repo-py
cd mono-repo-py

# Install uv if you haven't already
pip install uv

# Install all dependencies
uv sync
```

### Development

Install packages in development mode:

```bash
# Install all packages in development mode
uv pip install -e core
uv pip install -e api
uv pip install -e command-line
```

### Running the Demo

Start the API server:

```bash
uv run server
# Or with custom host/port
uv run server --host 127.0.0.1 --port 9000
# With debug logging
uv run server --debug
# Log to file
uv run server --log-file server.log
```

Use the command-line client:

```bash
uv run greet YourName
# Or with custom host/port
uv run greet YourName --host 127.0.0.1 --port 9000
# With debug logging
uv run greet YourName --debug
# Log to file
uv run greet YourName --log-file client.log
```

## Benefits of This Approach

1. **Modularity**: Each package can be developed, tested, and released independently
2. **Consistency**: Shared code ensures consistent behavior across packages
3. **Development Efficiency**: Changes to shared code immediately affect all packages
4. **Dependency Management**: UV handles complex dependencies between workspace packages
5. **Centralized Logging**: Common logging configuration and utilities across all packages

## Learn More

- [UV Documentation](https://github.com/astral-sh/uv)
- [Python Packaging User Guide](https://packaging.python.org)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
