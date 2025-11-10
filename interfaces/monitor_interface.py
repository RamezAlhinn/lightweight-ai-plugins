"""
System monitor interface for cross-platform resource monitoring.

This module defines the abstract interface that all platform-specific
monitors must implement. It demonstrates interface-based design and
the Strategy pattern for platform-specific implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class MemoryInfo:
    """
    Memory information dataclass.

    Attributes:
        total_gb: Total system memory in GB
        available_gb: Available memory in GB
        used_gb: Used memory in GB
        percent_used: Percentage of memory used (0-100)
    """
    total_gb: float
    available_gb: float
    used_gb: float
    percent_used: float


@dataclass
class CPUInfo:
    """
    CPU information dataclass.

    Attributes:
        percent_used: CPU usage percentage (0-100)
        core_count: Number of CPU cores
        frequency_mhz: Current CPU frequency in MHz (if available)
    """
    percent_used: float
    core_count: int
    frequency_mhz: Optional[float] = None


@dataclass
class BatteryInfo:
    """
    Battery information dataclass.

    Attributes:
        percent: Battery charge percentage (0-100)
        is_charging: Whether the battery is currently charging
        is_present: Whether a battery is present (False for desktops)
    """
    percent: Optional[float]
    is_charging: bool
    is_present: bool


@dataclass
class GPUInfo:
    """
    GPU information dataclass.

    Attributes:
        is_available: Whether a GPU is available
        name: GPU name/model (if available)
        memory_total_gb: Total GPU memory in GB (if available)
        memory_used_gb: Used GPU memory in GB (if available)
    """
    is_available: bool
    name: Optional[str] = None
    memory_total_gb: Optional[float] = None
    memory_used_gb: Optional[float] = None


class MonitorInterface(ABC):
    """
    Abstract base class for system resource monitors.

    All platform-specific monitors (Linux, Windows, Android) must
    implement this interface. This ensures consistent behavior across
    different platforms and allows the orchestrator to work with any
    platform without modification.

    Design Pattern: Strategy Pattern
    - MonitorInterface is the strategy interface
    - LinuxMonitor, WindowsMonitor, etc. are concrete strategies
    - ResourceSelector uses the strategy to make decisions
    """

    @abstractmethod
    def get_cpu_info(self) -> CPUInfo:
        """
        Get current CPU usage information.

        Returns:
            CPUInfo object with CPU usage data

        Raises:
            MonitorError: If CPU information cannot be retrieved

        Example:
            >>> monitor = get_platform_monitor()
            >>> cpu_info = monitor.get_cpu_info()
            >>> print(f"CPU usage: {cpu_info.percent_used}%")
        """
        pass

    @abstractmethod
    def get_memory_info(self) -> MemoryInfo:
        """
        Get current memory usage information.

        Returns:
            MemoryInfo object with memory usage data

        Raises:
            MonitorError: If memory information cannot be retrieved

        Example:
            >>> monitor = get_platform_monitor()
            >>> mem_info = monitor.get_memory_info()
            >>> print(f"Available memory: {mem_info.available_gb} GB")
        """
        pass

    @abstractmethod
    def get_battery_info(self) -> BatteryInfo:
        """
        Get current battery information.

        For desktop systems without a battery, this should return
        BatteryInfo with is_present=False.

        Returns:
            BatteryInfo object with battery data

        Raises:
            MonitorError: If battery information cannot be retrieved

        Example:
            >>> monitor = get_platform_monitor()
            >>> battery = monitor.get_battery_info()
            >>> if battery.is_present:
            >>>     print(f"Battery: {battery.percent}%")
        """
        pass

    @abstractmethod
    def get_gpu_info(self) -> GPUInfo:
        """
        Get GPU availability and information.

        For systems without a GPU, this should return
        GPUInfo with is_available=False.

        Returns:
            GPUInfo object with GPU data

        Raises:
            MonitorError: If GPU information cannot be retrieved

        Example:
            >>> monitor = get_platform_monitor()
            >>> gpu = monitor.get_gpu_info()
            >>> if gpu.is_available:
            >>>     print(f"GPU: {gpu.name}")
        """
        pass

    def get_all_info(self) -> Dict[str, Any]:
        """
        Get all system information at once.

        This is a convenience method that calls all other methods
        and returns the results as a dictionary. Implementations
        can override this for better performance if they can collect
        all data in one operation.

        Returns:
            Dictionary with keys: 'cpu', 'memory', 'battery', 'gpu'

        Example:
            >>> monitor = get_platform_monitor()
            >>> info = monitor.get_all_info()
            >>> print(f"CPU: {info['cpu'].percent_used}%")
            >>> print(f"Memory: {info['memory'].available_gb} GB")
        """
        return {
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'battery': self.get_battery_info(),
            'gpu': self.get_gpu_info(),
        }
