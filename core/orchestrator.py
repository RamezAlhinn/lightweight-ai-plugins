from core.resource_selector import select_model_type
from core.plugin_manager import load_plugin

def run_pipeline(input_data):
    model_type = select_model_type()
    plugin = load_plugin(model_type)
    plugin.load_model()
    return plugin.run(input_data)