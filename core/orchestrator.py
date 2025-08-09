from system import linux_monitor
from core import resource_selector, plugin_manager

if __name__ == "__main__":
    profile = linux_monitor.get_resource_profile()
    print(f"Profile: {profile}")

    choice = resource_selector.select_model(profile)
    print(f"Selected model: {choice}")

    plugin = plugin_manager.load_plugin(choice)
    result = plugin.predict("sample input")
    print(f"Result: {result}")