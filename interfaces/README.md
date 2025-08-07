# 🔗 interfaces/

This module defines shared **interfaces** and **abstract base classes** that all plugins must implement.

It ensures that all model plugins (light, medium, heavy) follow the same structure so the core can call them reliably.

---

## 🧠 Purpose

- Standardize plugin methods (e.g., `load_model()`, `predict()`)
- Enforce consistent structure across all AI plugins
- Enable dynamic plugin loading without tight coupling

---

## 📁 Typical Files

| File                  | Purpose                                |
|-----------------------|----------------------------------------|
| `plugin_interface.py` | Abstract class that all plugins must extend |

---

## 📦 Example: Plugin Interface

```python
# plugin_interface.py

from abc import ABC, abstractmethod

class PluginInterface(ABC):
    
    @abstractmethod
    def load_model(self):
        """Load the AI model into memory."""
        pass

    @abstractmethod
    def predict(self, input_data):
        """Run inference and return result."""
        pass