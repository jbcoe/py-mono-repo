"""Core package for shared functionality."""

from xyz.core.config import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_PROTOCOL,
    GREETING_ENDPOINT,
    ROOT_ENDPOINT,
)
from xyz.core.logging import configure_logging, get_logger, set_log_level

__all__ = [
    # Config
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "DEFAULT_PROTOCOL",
    "GREETING_ENDPOINT",
    "ROOT_ENDPOINT",
    # Logging
    "configure_logging",
    "get_logger",
    "set_log_level",
]
