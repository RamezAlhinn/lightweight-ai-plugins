# 🖥️ system/

This module monitors the device’s system resources and provides data to help the core module decide which AI plugin to use.

---

## 🧠 Purpose

The system module tracks real-time hardware usage to:
- Detect CPU usage
- Monitor battery level
- Measure RAM or GPU load (if available)
- Feed these metrics into the `core` for smart model selection

---

## ⚙️ Key Responsibilities

- `get_system_status()` → returns a summary of current hardware stats
- Acts as a dependency-free hardware health reporter
- Can be extended later for IoT/edge-specific metrics

---

## 🧪 Sample Output

```python
{
  "battery": 45,          # percent
  "cpu_load": 67,         # percent
  "ram_available": 30,    # percent
  "gpu_load": None        # (optional)
}
