from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def run(self, input_data):
        pass
