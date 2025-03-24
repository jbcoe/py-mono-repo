"""Logging configuration for the xyz projects."""

import logging
import sys
from typing import Literal, Optional, Union

LogLevel = Union[int, Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]]

# Default format includes timestamp, level, module, and message
DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)


def configure_logging(
    level: LogLevel = "INFO",
    format_str: Optional[str] = None,
    date_format: Optional[str] = None,
    log_file: Optional[str] = None,
) -> None:
    """Configure logging for the application.

    Args:
        level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_str: The log format string (defaults to DEFAULT_FORMAT)
        date_format: The date format string (defaults to DEFAULT_DATE_FORMAT)
        log_file: Optional file path to write logs to
    """
    if isinstance(level, str):
        level = getattr(logging, level)

    # Set up the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates when reconfiguring
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure formatter
    formatter = logging.Formatter(
        format_str or DEFAULT_FORMAT, date_format or DEFAULT_DATE_FORMAT
    )

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Optionally configure file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Log configuration info at debug level
    root_logger.debug(f"Logging configured with level={logging.getLevelName(level)}")
    if log_file:
        root_logger.debug(f"Logging to file: {log_file}")


def set_log_level(level: LogLevel) -> None:
    """Set the logging level for the root logger.

    Args:
        level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if isinstance(level, str):
        level = getattr(logging, level)

    logging.getLogger().setLevel(level)
    logging.debug(f"Log level set to {logging.getLevelName(level)}")
