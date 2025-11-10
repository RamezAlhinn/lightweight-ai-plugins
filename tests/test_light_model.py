"""
Unit tests for the light model plugin.

These tests demonstrate:
- Testing plugin implementations
- Testing model lifecycle (load/run/unload)
- Exception handling tests
"""
import pytest
from plugins.light_model import LightModelPlugin
from core.exceptions import InvalidInputError


def test_light_model_initialization():
    """Test that LightModelPlugin initializes correctly."""
    plugin = LightModelPlugin()
    assert plugin is not None
    assert plugin.is_loaded is False
    assert plugin.model is None


def test_light_model_load():
    """Test loading the light model."""
    plugin = LightModelPlugin()
    plugin.load_model()
    assert plugin.is_loaded is True
    assert plugin.model is not None


def test_light_model_run():
    """Test running inference with the light model."""
    plugin = LightModelPlugin()
    plugin.load_model()

    result = plugin.run("test input")
    assert result is not None
    assert isinstance(result, str)
    assert "LIGHT" in result
    assert "test input" in result


def test_light_model_run_without_load():
    """Test that running without loading raises an error."""
    plugin = LightModelPlugin()

    with pytest.raises(RuntimeError) as exc_info:
        plugin.run("test input")

    assert "not loaded" in str(exc_info.value).lower()


def test_light_model_empty_input():
    """Test that empty input raises InvalidInputError."""
    plugin = LightModelPlugin()
    plugin.load_model()

    with pytest.raises(InvalidInputError):
        plugin.run("")


def test_light_model_unload():
    """Test unloading the light model."""
    plugin = LightModelPlugin()
    plugin.load_model()
    assert plugin.is_loaded is True

    plugin.unload_model()
    assert plugin.is_loaded is False
    assert plugin.model is None


def test_light_model_get_info():
    """Test getting model information."""
    plugin = LightModelPlugin()
    info = plugin.get_model_info()

    assert isinstance(info, dict)
    assert info["name"] == "Light Model"
    assert info["type"] == "light"
    assert "version" in info
