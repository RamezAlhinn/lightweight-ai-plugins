from interfaces.plugin_interface import PluginInterface

class LightModelPlugin(PluginInterface):
    def load_model(self):
        print("Light model loaded (dummy).")

    def run(self, input_data):
        print(f"Running light model on input: {input_data}")
        return "output"
