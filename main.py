import platform
from core import resource_selector, plugin_manager

def _monitor():
    osname = platform.system()
    if osname == "Linux":
        from system import linux_monitor as mon
    elif osname == "Windows":
        from system import windows_monitor as mon
    elif osname == "Darwin":  # macOS
        from system import linux_monitor as mon  # TODO here its just a temperoory fix
    else:
        from system import linux_monitor as mon
    return mon

def main():
    print("=== Lightweight AI Plugins MVP ===")
    mon = _monitor()
    profile = mon.get_resource_profile()
    print(f"Resource profile: {profile}")

    selected = resource_selector.select_model(profile)
    print(f"Selected plugin: {selected}")

    plugin = plugin_manager.load_plugin(selected)
    result = plugin.predict("sample input")
    print(f"Result from {selected}: {result}")

if __name__ == "__main__":
    main()