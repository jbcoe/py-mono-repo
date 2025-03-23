"""Configuration module for shared settings across packages."""

# Default server settings
DEFAULT_HOST = "0.0.0.0"  # Binds to all network interfaces
DEFAULT_PORT = 8000

# Client settings
DEFAULT_PROTOCOL = "http"

# API paths
GREETING_ENDPOINT = "/greet/{name}"
ROOT_ENDPOINT = "/"
