"""
Unit tests for the plugin manager.

These tests demonstrate:
- Unit testing with pytest
- Testing dynamic imports
- Mocking and fixtures
- Exception testing
"""
import pytest
from core.plugin_manager import load_plugin, get_available_plugins
from core.exceptions import PluginNotFoundError
from interfaces.plugin_interface import PluginInterface


def test_get_available_plugins():
    """Test that available plugins are correctly listed."""
    plugins = get_available_plugins()
    assert isinstance(plugins, list)
    assert "light" in plugins
    assert "medium" in plugins
    assert "heavy" in plugins


def test_load_light_plugin():
    """Test loading the light model plugin."""
    plugin = load_plugin("light")
    assert plugin is not None
    assert isinstance(plugin, PluginInterface)


def test_load_invalid_plugin():
    """Test that loading an invalid plugin raises PluginNotFoundError."""
    with pytest.raises(PluginNotFoundError) as exc_info:
        load_plugin("nonexistent")

    assert "No plugin found" in str(exc_info.value)
    assert "nonexistent" in str(exc_info.value)


def test_plugin_caching():
    """Test that plugins are cached when requested."""
    plugin1 = load_plugin("light", use_cache=True)
    plugin2 = load_plugin("light", use_cache=True)

    # Should be the same instance when cached
    assert plugin1 is plugin2


def test_plugin_no_cache():
    """Test loading plugins without caching."""
    plugin1 = load_plugin("light", use_cache=False)
    plugin2 = load_plugin("light", use_cache=False)

    # Should be different instances when not cached
    assert plugin1 is not plugin2
