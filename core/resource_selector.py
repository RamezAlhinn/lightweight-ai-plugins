"""
Resource-aware model selector.

This module implements the decision logic for selecting the most appropriate
AI model based on current system resources. It follows the flowchart defined
in the README and demonstrates decision-making algorithms.

Decision Flow (from README):
1. Check battery level: < 30% → light model
2. Check available RAM: < 2 GB → light model
3. Check CPU usage: > 80% → light model
4. Check GPU availability:
   - GPU available + sufficient resources → heavy model
   - Otherwise → medium model
"""
import platform
from typing import Literal

from interfaces.monitor_interface import MonitorInterface
from system.linux_monitor import LinuxMonitor
from core.exceptions import MonitorError, InsufficientResourcesError
from utils.logger import get_logger

logger = get_logger(__name__)

# Type alias for model types
ModelType = Literal["light", "medium", "heavy"]

# Default thresholds (can be made configurable later)
BATTERY_LOW_THRESHOLD = 30.0  # percent
RAM_MINIMUM_GB = 2.0          # gigabytes
CPU_HIGH_THRESHOLD = 80.0     # percent
RAM_HEAVY_MODEL_GB = 4.0      # GB needed for heavy model


def get_platform_monitor() -> MonitorInterface:
    """
    Get the appropriate system monitor for the current platform.

    Returns:
        Platform-specific monitor instance

    Raises:
        MonitorError: If platform is not supported

    Example:
        >>> monitor = get_platform_monitor()
        >>> cpu_info = monitor.get_cpu_info()
    """
    system = platform.system()
    logger.debug(f"Detecting platform: {system}")

    if system == "Linux":
        logger.info("Using LinuxMonitor")
        return LinuxMonitor()
    elif system == "Windows":
        # For now, fall back to LinuxMonitor (psutil works on Windows too)
        # In a complete implementation, use WindowsMonitor
        logger.warning("Windows platform detected, using cross-platform psutil monitor")
        return LinuxMonitor()
    elif system == "Darwin":  # macOS
        logger.warning("macOS platform detected, using cross-platform psutil monitor")
        return LinuxMonitor()
    else:
        raise MonitorError(f"Unsupported platform: {system}")


def select_model_type(
    battery_threshold: float = BATTERY_LOW_THRESHOLD,
    ram_minimum_gb: float = RAM_MINIMUM_GB,
    cpu_threshold: float = CPU_HIGH_THRESHOLD,
    ram_heavy_gb: float = RAM_HEAVY_MODEL_GB
) -> ModelType:
    """
    Select the most appropriate model type based on system resources.

    This function implements the resource-aware selection algorithm:
    1. Low battery (< 30%) → light model (save power)
    2. Low RAM (< 2 GB) → light model (prevent OOM)
    3. High CPU (> 80%) → light model (system is busy)
    4. GPU available + enough RAM (> 4 GB) → heavy model (use GPU)
    5. Otherwise → medium model (balanced choice)

    The thresholds can be customized via parameters for testing or
    different deployment scenarios.

    Args:
        battery_threshold: Battery percentage below which to use light model
        ram_minimum_gb: Minimum RAM in GB to run any model
        cpu_threshold: CPU usage percentage above which to use light model
        ram_heavy_gb: Minimum RAM in GB needed for heavy model

    Returns:
        Model type: "light", "medium", or "heavy"

    Raises:
        InsufficientResourcesError: If resources are too low for any model
        MonitorError: If system monitoring fails

    Example:
        >>> model = select_model_type()
        >>> print(f"Selected: {model}")
        Selected: medium

        >>> # Custom thresholds for testing
        >>> model = select_model_type(battery_threshold=20, ram_minimum_gb=1)
    """
    logger.info("=" * 60)
    logger.info("Starting resource-aware model selection")
    logger.info("=" * 60)

    try:
        # Get platform-specific monitor
        monitor = get_platform_monitor()

        # Collect system information
        logger.info("Collecting system resource information...")

        cpu_info = monitor.get_cpu_info()
        memory_info = monitor.get_memory_info()
        battery_info = monitor.get_battery_info()
        gpu_info = monitor.get_gpu_info()

        # Log current system state
        logger.info(f"CPU Usage: {cpu_info.percent_used}% ({cpu_info.core_count} cores)")
        logger.info(
            f"Memory: {memory_info.available_gb}/{memory_info.total_gb} GB available "
            f"({memory_info.percent_used}% used)"
        )

        if battery_info.is_present:
            logger.info(
                f"Battery: {battery_info.percent}% "
                f"({'charging' if battery_info.is_charging else 'not charging'})"
            )
        else:
            logger.info("Battery: Not present (desktop/plugged system)")

        logger.info(
            f"GPU: {'Available' if gpu_info.is_available else 'Not available'}"
            + (f" ({gpu_info.name})" if gpu_info.name else "")
        )

        # Decision tree starts here
        logger.info("\nApplying selection criteria...")

        # Check 0: Absolute minimum resources
        if memory_info.available_gb < 0.5:  # Less than 500 MB
            raise InsufficientResourcesError(
                f"Critically low memory: {memory_info.available_gb} GB available. "
                "Cannot safely run any model."
            )

        # Check 1: Battery level (if present)
        if battery_info.is_present and not battery_info.is_charging:
            if battery_info.percent and battery_info.percent < battery_threshold:
                logger.info(
                    f"✓ Battery low ({battery_info.percent}% < {battery_threshold}%) "
                    "→ Selecting LIGHT model to conserve power"
                )
                return "light"

        # Check 2: Available RAM
        if memory_info.available_gb < ram_minimum_gb:
            logger.info(
                f"✓ Low available RAM ({memory_info.available_gb} GB < {ram_minimum_gb} GB) "
                "→ Selecting LIGHT model to prevent out-of-memory"
            )
            return "light"

        # Check 3: CPU usage
        if cpu_info.percent_used > cpu_threshold:
            logger.info(
                f"✓ High CPU usage ({cpu_info.percent_used}% > {cpu_threshold}%) "
                "→ Selecting LIGHT model to reduce system load"
            )
            return "light"

        # Check 4: GPU availability and sufficient resources for heavy model
        if gpu_info.is_available and memory_info.available_gb >= ram_heavy_gb:
            logger.info(
                f"✓ GPU available and sufficient RAM ({memory_info.available_gb} GB >= {ram_heavy_gb} GB) "
                "→ Selecting HEAVY model for best performance"
            )
            return "heavy"

        # Default: Medium model
        logger.info(
            "✓ Resources are moderate (no GPU or insufficient RAM for heavy model) "
            "→ Selecting MEDIUM model for balanced performance"
        )
        return "medium"

    except InsufficientResourcesError:
        # Re-raise critical errors
        raise

    except Exception as e:
        # If monitoring fails, fall back to light model (safest option)
        logger.error(f"Resource monitoring failed: {e}")
        logger.warning("Falling back to LIGHT model due to monitoring error")
        return "light"

    finally:
        logger.info("=" * 60)
