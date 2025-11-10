"""
Centralized logging configuration for the Lightweight AI Plugin Framework.

This module provides a consistent logging setup across all modules,
demonstrating logging best practices for students.
"""
import logging
import sys
from pathlib import Path
from typing import Optional


# Default log format - shows timestamp, logger name, level, and message
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Global logging configuration
_initialized = False
_log_level = logging.INFO
_log_file: Optional[Path] = None


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> None:
    """
    Configure the root logger for the application.

    This should be called once at application startup. It sets up:
    - Console handler (stderr) for real-time output
    - Optional file handler for persistent logs
    - Consistent formatting across all loggers

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
        log_file: Optional path to log file. If provided, logs will be written to this file
        console: Whether to output logs to console (default: True)

    Example:
        >>> setup_logging(level=logging.DEBUG, log_file="app.log")
    """
    global _initialized, _log_level, _log_file

    if _initialized:
        return

    _log_level = level
    _log_file = Path(log_file) if log_file else None

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)

    # Console handler (stderr)
    if console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # File handler (if specified)
    if _log_file:
        # Create log directory if it doesn't exist
        _log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(_log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    This is the recommended way to get loggers in the application.
    Each module should call this with __name__ to get a properly
    namespaced logger.

    Args:
        name: Logger name (typically __name__ of the calling module)

    Returns:
        A configured Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Starting process")
        >>> logger.debug("Debug information")
        >>> logger.error("An error occurred")
    """
    # Initialize with defaults if not already initialized
    if not _initialized:
        setup_logging()

    return logging.getLogger(name)


def set_level(level: int) -> None:
    """
    Change the logging level at runtime.

    Args:
        level: New logging level (e.g., logging.DEBUG, logging.INFO)

    Example:
        >>> set_level(logging.DEBUG)  # Enable debug output
    """
    global _log_level
    _log_level = level

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Update all handlers
    for handler in root_logger.handlers:
        handler.setLevel(level)


def get_level() -> int:
    """
    Get the current logging level.

    Returns:
        Current logging level as an integer
    """
    return _log_level
