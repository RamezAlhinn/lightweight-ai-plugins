"""
Plugin interface for AI model plugins.

This module defines the abstract interface that all AI model plugins
must implement. It ensures consistent behavior across different model
types and demonstrates the Strategy pattern.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class PluginInterface(ABC):
    """
    Abstract base class for AI model plugins.

    All plugin implementations (light, medium, heavy) must inherit from
    this class and implement all abstract methods. This ensures that
    the orchestrator can work with any plugin without knowing its
    specific implementation details.

    Design Pattern: Strategy Pattern
    - PluginInterface is the strategy interface
    - LightModelPlugin, MediumModelPlugin, HeavyModelPlugin are concrete strategies
    - Orchestrator uses the strategy to execute AI tasks

    Example:
        >>> class MyModelPlugin(PluginInterface):
        ...     def load_model(self) -> None:
        ...         # Load model implementation
        ...         pass
        ...
        ...     def run(self, input_data: str) -> Any:
        ...         # Inference implementation
        ...         return result
    """

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the AI model into memory.

        This method should:
        - Load model weights from disk
        - Initialize the model
        - Prepare it for inference
        - Set up any required resources

        Raises:
            ModelLoadError: If model loading fails
            FileNotFoundError: If model file is missing

        Example:
            >>> plugin = LightModelPlugin()
            >>> plugin.load_model()
        """
        pass

    @abstractmethod
    def run(self, input_data: str) -> Any:
        """
        Run inference on the input data.

        This method performs the actual AI computation. The input and
        output types depend on the specific model task (e.g., text
        classification, object detection, etc.).

        Args:
            input_data: Input data to process. Format depends on the model.

        Returns:
            Model output. Type and format depend on the model task.

        Raises:
            InvalidInputError: If input_data is invalid
            RuntimeError: If inference fails

        Example:
            >>> plugin = LightModelPlugin()
            >>> plugin.load_model()
            >>> result = plugin.run("Hello world")
            >>> print(result)
        """
        pass

    def unload_model(self) -> None:
        """
        Unload the model and free resources.

        This method is optional but recommended. It should:
        - Free model memory
        - Release GPU resources
        - Close any open files
        - Clean up temporary data

        Default implementation does nothing. Override if your plugin
        needs cleanup.

        Example:
            >>> plugin = LightModelPlugin()
            >>> plugin.load_model()
            >>> # ... use model ...
            >>> plugin.unload_model()
        """
        pass

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model.

        Returns metadata about the model such as name, version,
        size, and capabilities.

        Returns:
            Dictionary with model metadata

        Example:
            >>> plugin = LightModelPlugin()
            >>> info = plugin.get_model_info()
            >>> print(info['name'])
            'Light Model'
        """
        return {
            'name': self.__class__.__name__,
            'type': 'unknown',
            'version': '1.0.0',
        }
