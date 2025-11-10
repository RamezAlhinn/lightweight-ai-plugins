"""
Plugin manager for dynamic loading and management of AI model plugins.

This module handles:
- Plugin discovery and loading
- Plugin registry management
- Plugin lifecycle management (load/unload)
- Plugin caching for performance

It demonstrates the Plugin pattern and dynamic importing in Python.
"""
import importlib
from typing import Dict, Type, Optional, List

from interfaces.plugin_interface import PluginInterface
from core.exceptions import PluginNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)

# Plugin registry: maps model type names to their module paths
# Format: "plugin_name": "module.path.ClassName"
PLUGIN_REGISTRY: Dict[str, str] = {
    "light": "plugins.light_model.LightModelPlugin",
    "medium": "plugins.medium_model.MediumModelPlugin",
    "heavy": "plugins.heavy_model.HeavyModelPlugin",
}

# Plugin cache: stores loaded plugin instances to avoid reloading
# This is a simple optimization - in production, you might use LRU cache
_plugin_cache: Dict[str, PluginInterface] = {}


def load_plugin(name: str, use_cache: bool = True) -> PluginInterface:
    """
    Load a plugin by name using dynamic importing.

    This function demonstrates:
    - Dynamic module importing with importlib
    - Plugin registry pattern
    - Caching for performance
    - Comprehensive error handling

    Args:
        name: Plugin name (one of "light", "medium", "heavy")
        use_cache: Whether to use cached plugin instance if available.
                  Set to False to force reload.

    Returns:
        An instance of the requested plugin implementing PluginInterface

    Raises:
        PluginNotFoundError: If the plugin doesn't exist or can't be loaded
        TypeError: If the loaded class doesn't implement PluginInterface

    Example:
        >>> plugin = load_plugin("light")
        >>> plugin.load_model()
        >>> result = plugin.run("input data")

        >>> # Force reload without cache
        >>> plugin = load_plugin("light", use_cache=False)
    """
    # Check cache first (if enabled)
    if use_cache and name in _plugin_cache:
        logger.debug(f"Using cached plugin: {name}")
        return _plugin_cache[name]

    # Validate plugin name exists in registry
    if name not in PLUGIN_REGISTRY:
        available = ", ".join(PLUGIN_REGISTRY.keys())
        logger.error(
            f"Plugin '{name}' not found. Available plugins: {available}"
        )
        raise PluginNotFoundError(
            f"No plugin found for '{name}'. Available plugins: {available}"
        )

    # Get module path from registry
    module_path = PLUGIN_REGISTRY[name]
    logger.debug(f"Plugin registry entry: {name} -> {module_path}")

    # Split into module name and class name
    # e.g., "plugins.light_model.LightModelPlugin"
    #       -> "plugins.light_model", "LightModelPlugin"
    try:
        module_name, class_name = module_path.rsplit(".", 1)
    except ValueError:
        raise PluginNotFoundError(
            f"Invalid plugin path format in registry: {module_path}"
        )

    try:
        # Dynamically import the module
        logger.info(f"Loading plugin '{name}' from {module_path}")
        module = importlib.import_module(module_name)
        logger.debug(f"Module {module_name} imported successfully")

        # Get the plugin class from the module
        if not hasattr(module, class_name):
            raise PluginNotFoundError(
                f"Class '{class_name}' not found in module '{module_name}'"
            )

        plugin_class: Type[PluginInterface] = getattr(module, class_name)
        logger.debug(f"Class {class_name} retrieved from module")

        # Validate that the class implements PluginInterface
        if not issubclass(plugin_class, PluginInterface):
            raise TypeError(
                f"{class_name} does not implement PluginInterface. "
                f"All plugins must inherit from PluginInterface."
            )

        # Instantiate the plugin
        plugin = plugin_class()
        logger.info(f"Plugin '{name}' loaded successfully: {class_name}")

        # Cache the instance (if enabled)
        if use_cache:
            _plugin_cache[name] = plugin
            logger.debug(f"Plugin '{name}' cached for future use")

        return plugin

    except ImportError as e:
        logger.error(f"Failed to import plugin module '{module_name}': {e}")
        raise PluginNotFoundError(
            f"Failed to import plugin '{name}': {e}"
        ) from e

    except AttributeError as e:
        logger.error(f"Plugin class '{class_name}' not found in module: {e}")
        raise PluginNotFoundError(
            f"Plugin class '{class_name}' not found in module '{module_name}': {e}"
        ) from e


def unload_plugin(plugin: PluginInterface) -> None:
    """
    Unload a plugin and clean up its resources.

    This calls the plugin's cleanup methods and removes it from cache.

    Args:
        plugin: The plugin instance to unload

    Example:
        >>> plugin = load_plugin("light")
        >>> # ... use plugin ...
        >>> unload_plugin(plugin)
    """
    try:
        plugin_name = type(plugin).__name__
        logger.debug(f"Unloading plugin: {plugin_name}")

        # Call plugin cleanup if available
        if hasattr(plugin, 'unload_model'):
            plugin.unload_model()
            logger.debug(f"Plugin {plugin_name} unload_model() called")

        # Remove from cache if present
        cache_key = None
        for key, cached_plugin in _plugin_cache.items():
            if cached_plugin is plugin:
                cache_key = key
                break

        if cache_key:
            del _plugin_cache[cache_key]
            logger.debug(f"Plugin '{cache_key}' removed from cache")

        logger.info(f"Plugin {plugin_name} unloaded successfully")

    except Exception as e:
        logger.warning(f"Error unloading plugin: {e}")


def clear_cache() -> None:
    """
    Clear the plugin cache and unload all cached plugins.

    This is useful for:
    - Freeing memory
    - Forcing plugin reload
    - Application shutdown

    Example:
        >>> clear_cache()  # Unload all cached plugins
    """
    logger.info(f"Clearing plugin cache ({len(_plugin_cache)} plugins)")

    # Unload each cached plugin
    for plugin in list(_plugin_cache.values()):
        try:
            unload_plugin(plugin)
        except Exception as e:
            logger.warning(f"Error unloading cached plugin: {e}")

    _plugin_cache.clear()
    logger.info("Plugin cache cleared")


def get_available_plugins() -> List[str]:
    """
    Get a list of all available plugin names.

    Returns:
        List of plugin names that can be loaded

    Example:
        >>> plugins = get_available_plugins()
        >>> print(plugins)
        ['light', 'medium', 'heavy']
    """
    return list(PLUGIN_REGISTRY.keys())


def is_plugin_cached(name: str) -> bool:
    """
    Check if a plugin is currently cached.

    Args:
        name: Plugin name to check

    Returns:
        True if the plugin is in cache, False otherwise

    Example:
        >>> load_plugin("light")
        >>> is_plugin_cached("light")
        True
        >>> is_plugin_cached("heavy")
        False
    """
    return name in _plugin_cache
