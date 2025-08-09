import importlib

def load_plugin(plugin_name):
    module = importlib.import_module(f"plugins.{plugin_name}")
    return module.ModelPlugin()