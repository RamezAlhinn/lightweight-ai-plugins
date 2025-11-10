"""
Linux-specific system resource monitor.

This module implements the MonitorInterface for Linux systems using psutil
and Linux-specific system files (/sys, /proc). It demonstrates:
- Platform-specific implementations
- Using psutil for system monitoring
- Reading Linux system files
- Error handling for missing resources
"""
import os
import psutil
from pathlib import Path
from typing import Optional

from interfaces.monitor_interface import (
    MonitorInterface,
    CPUInfo,
    MemoryInfo,
    BatteryInfo,
    GPUInfo
)
from core.exceptions import MonitorError
from utils.logger import get_logger

logger = get_logger(__name__)


class LinuxMonitor(MonitorInterface):
    """
    Linux system resource monitor implementation.

    Uses psutil for cross-platform metrics and Linux-specific files
    for additional information. This implementation works on any
    Linux distribution including Ubuntu, Debian, Fedora, Arch, etc.

    Example:
        >>> monitor = LinuxMonitor()
        >>> cpu_info = monitor.get_cpu_info()
        >>> print(f"CPU Usage: {cpu_info.percent_used}%")
    """

    def __init__(self):
        """Initialize the Linux monitor."""
        logger.debug("Initializing LinuxMonitor")

        # Verify we're on Linux
        if not self._is_linux():
            logger.warning("LinuxMonitor initialized on non-Linux platform")

    @staticmethod
    def _is_linux() -> bool:
        """Check if running on Linux."""
        return os.name == 'posix' and os.uname().sysname == 'Linux'

    def get_cpu_info(self) -> CPUInfo:
        """
        Get current CPU usage information.

        Returns:
            CPUInfo with CPU usage, core count, and frequency

        Raises:
            MonitorError: If CPU information cannot be retrieved
        """
        try:
            logger.debug("Fetching CPU information")

            # Get CPU usage percentage (averaged over 1 second)
            # Using interval=1 for more accurate reading
            cpu_percent = psutil.cpu_percent(interval=1.0)

            # Get number of CPU cores
            core_count = psutil.cpu_count(logical=True)

            # Get CPU frequency (if available)
            frequency_mhz = None
            try:
                freq = psutil.cpu_freq()
                if freq:
                    frequency_mhz = freq.current
            except Exception as e:
                logger.debug(f"CPU frequency not available: {e}")

            cpu_info = CPUInfo(
                percent_used=cpu_percent,
                core_count=core_count if core_count else 1,
                frequency_mhz=frequency_mhz
            )

            logger.debug(
                f"CPU Info: {cpu_info.percent_used}% used, "
                f"{cpu_info.core_count} cores"
            )

            return cpu_info

        except Exception as e:
            logger.error(f"Failed to get CPU info: {e}")
            raise MonitorError(f"Cannot retrieve CPU information: {e}") from e

    def get_memory_info(self) -> MemoryInfo:
        """
        Get current memory usage information.

        Returns:
            MemoryInfo with total, available, used memory and usage percentage

        Raises:
            MonitorError: If memory information cannot be retrieved
        """
        try:
            logger.debug("Fetching memory information")

            # Get virtual memory stats
            mem = psutil.virtual_memory()

            # Convert bytes to GB
            total_gb = mem.total / (1024 ** 3)
            available_gb = mem.available / (1024 ** 3)
            used_gb = mem.used / (1024 ** 3)
            percent_used = mem.percent

            memory_info = MemoryInfo(
                total_gb=round(total_gb, 2),
                available_gb=round(available_gb, 2),
                used_gb=round(used_gb, 2),
                percent_used=percent_used
            )

            logger.debug(
                f"Memory Info: {memory_info.available_gb}/{memory_info.total_gb} GB available "
                f"({memory_info.percent_used}% used)"
            )

            return memory_info

        except Exception as e:
            logger.error(f"Failed to get memory info: {e}")
            raise MonitorError(f"Cannot retrieve memory information: {e}") from e

    def get_battery_info(self) -> BatteryInfo:
        """
        Get current battery information.

        For desktop systems without a battery, returns BatteryInfo
        with is_present=False.

        Returns:
            BatteryInfo with battery percentage, charging status, and presence

        Raises:
            MonitorError: If battery information cannot be retrieved
        """
        try:
            logger.debug("Fetching battery information")

            # Try to get battery info
            battery = psutil.sensors_battery()

            if battery is None:
                # No battery present (desktop system)
                logger.debug("No battery detected (desktop system)")
                return BatteryInfo(
                    percent=None,
                    is_charging=False,
                    is_present=False
                )

            battery_info = BatteryInfo(
                percent=round(battery.percent, 1),
                is_charging=battery.power_plugged,
                is_present=True
            )

            logger.debug(
                f"Battery Info: {battery_info.percent}% "
                f"({'charging' if battery_info.is_charging else 'discharging'})"
            )

            return battery_info

        except Exception as e:
            logger.error(f"Failed to get battery info: {e}")
            raise MonitorError(f"Cannot retrieve battery information: {e}") from e

    def get_gpu_info(self) -> GPUInfo:
        """
        Get GPU availability and information.

        This is a basic implementation that checks for common GPU indicators.
        For production use, consider using libraries like pynvml (NVIDIA),
        py3nvml, or GPUtil for more detailed information.

        Returns:
            GPUInfo with GPU availability and basic info

        Raises:
            MonitorError: If GPU information cannot be retrieved
        """
        try:
            logger.debug("Fetching GPU information")

            # Basic check: look for GPU device files
            gpu_available = False
            gpu_name = None

            # Check for NVIDIA GPU
            if Path("/dev/nvidia0").exists():
                gpu_available = True
                gpu_name = "NVIDIA GPU"
                logger.debug("NVIDIA GPU detected")

            # Check for AMD GPU
            elif Path("/dev/dri").exists():
                dri_devices = list(Path("/dev/dri").glob("card*"))
                if dri_devices:
                    gpu_available = True
                    gpu_name = "GPU (DRI)"
                    logger.debug("DRI GPU detected")

            # Try to get more info from lspci if available
            if gpu_available:
                try:
                    import subprocess
                    result = subprocess.run(
                        ['lspci'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    for line in result.stdout.splitlines():
                        if 'VGA' in line or 'Display' in line or '3D' in line:
                            # Extract GPU name
                            if ':' in line:
                                gpu_name = line.split(':', 1)[1].strip()
                                break
                except Exception as e:
                    logger.debug(f"lspci not available: {e}")

            gpu_info = GPUInfo(
                is_available=gpu_available,
                name=gpu_name,
                memory_total_gb=None,  # Would need nvidia-smi or similar
                memory_used_gb=None
            )

            logger.debug(
                f"GPU Info: {'Available' if gpu_info.is_available else 'Not available'}"
                + (f" ({gpu_info.name})" if gpu_info.name else "")
            )

            return gpu_info

        except Exception as e:
            logger.error(f"Failed to get GPU info: {e}")
            # Don't raise - just return unavailable
            return GPUInfo(is_available=False)
