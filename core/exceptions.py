"""
Custom exception hierarchy for the Lightweight AI Plugin Framework.

This module defines specific exceptions for different failure modes,
making error handling more precise and informative for students learning
about exception handling best practices.
"""


class PluginError(Exception):
    """
    Base exception for all plugin-related errors.

    This is the parent class for all custom exceptions in the framework.
    Catching this exception will catch all framework-specific errors.
    """
    pass


class PluginNotFoundError(PluginError):
    """
    Raised when a requested plugin cannot be found or loaded.

    This typically occurs when:
    - An invalid plugin name is specified
    - The plugin module is missing or cannot be imported
    - The plugin class is not found in the module
    """
    pass


class ModelLoadError(PluginError):
    """
    Raised when a model fails to load.

    This can happen due to:
    - Missing model file
    - Corrupted model file
    - Insufficient memory
    - Incompatible model format
    """
    pass


class InsufficientResourcesError(PluginError):
    """
    Raised when system resources are too low to run any model.

    This is a critical error indicating that even the lightest
    model cannot be loaded safely.
    """
    pass


class InvalidInputError(PluginError):
    """
    Raised when input data is invalid or cannot be processed.

    This includes:
    - Wrong data type
    - Malformed input
    - Out of range values
    - Missing required fields
    """
    pass


class MonitorError(Exception):
    """
    Base exception for system monitoring errors.

    Raised when system resource monitoring fails.
    """
    pass


class MonitorNotAvailableError(MonitorError):
    """
    Raised when a system monitor is not available for the current platform.

    For example, trying to use LinuxMonitor on Windows.
    """
    pass
