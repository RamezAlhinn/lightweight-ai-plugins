# Test Suite

This directory contains tests for the Lightweight AI Plugin Framework.

## Running Tests

### Install test dependencies:

```bash
pip install pytest pytest-cov
```

### Run all tests:

```bash
pytest
```

### Run with coverage:

```bash
pytest --cov=. --cov-report=html
```

### Run specific test file:

```bash
pytest tests/test_plugin_manager.py
```

### Run with verbose output:

```bash
pytest -v
```

## Test Structure

- `test_plugin_manager.py` - Tests for plugin loading and management
- `test_light_model.py` - Tests for the light model plugin
- More test files can be added for:
  - `test_orchestrator.py` - Pipeline orchestration
  - `test_resource_selector.py` - Resource-aware selection
  - `test_monitors.py` - System monitoring
  - `test_integration.py` - End-to-end integration tests

## Writing Tests

Example test:

```python
import pytest
from core.plugin_manager import load_plugin

def test_load_plugin():
    """Test loading a plugin."""
    plugin = load_plugin("light")
    assert plugin is not None
```

## Test Coverage Goals

- Aim for >80% code coverage
- Test all error paths
- Test edge cases
- Write integration tests for critical paths
