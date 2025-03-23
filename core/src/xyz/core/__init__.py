"""Core package for shared functionality."""

from xyz.core.config import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_CLIENT_HOST,
    DEFAULT_CLIENT_PORT,
    DEFAULT_PROTOCOL,
    GREETING_ENDPOINT,
    ROOT_ENDPOINT,
)


def hello() -> str:
    return "Hello from core!"
