"""Configuration module for shared settings across packages."""

# Default server settings
DEFAULT_HOST = "0.0.0.0"  # Binds to all network interfaces
DEFAULT_PORT = 8000

# Client default settings
DEFAULT_CLIENT_HOST = "localhost"  # For client connections
DEFAULT_CLIENT_PORT = 8000
DEFAULT_PROTOCOL = "http"

# API paths
GREETING_ENDPOINT = "/greet/{name}"
ROOT_ENDPOINT = "/"
