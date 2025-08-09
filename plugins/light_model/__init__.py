from interfaces.plugin_interface import PluginInterface

class ModelPlugin:
    def __init__(self):
        self.name = "Light Model"
        # Load pre-trained model here (e.g., TFLite interpreter)
    def predict(self, input_data):
        return "Predicted: light result"