"""
Medium model plugin implementation.

This plugin provides a medium-sized AI model suitable for:
- Balanced performance and resource usage
- Standard desktop/laptop environments
- Moderate accuracy requirements

For educational purposes, this is a dummy implementation similar to LightModelPlugin.
"""
from typing import Any, Dict
from pathlib import Path

from interfaces.plugin_interface import PluginInterface
from core.exceptions import ModelLoadError, InvalidInputError
from utils.logger import get_logger

logger = get_logger(__name__)


class MediumModelPlugin(PluginInterface):
    """Medium-sized AI model plugin (dummy implementation)."""

    def __init__(self):
        """Initialize the medium model plugin."""
        logger.debug("Initializing MediumModelPlugin")
        self.model_path = Path("models/medium.tflite")
        self.is_loaded = False
        self.model = None
        logger.info("MediumModelPlugin initialized")

    def load_model(self) -> None:
        """Load the medium model into memory."""
        try:
            logger.info("Loading medium model...")
            logger.debug(f"Model path: {self.model_path}")

            # Dummy implementation
            logger.debug("Simulating model loading (dummy implementation)")
            self.model = "dummy_medium_model"
            self.is_loaded = True

            logger.info(" Medium model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load medium model: {e}")
            raise ModelLoadError(f"Medium model loading failed: {e}") from e

    def run(self, input_data: str) -> Any:
        """Run inference on the input data."""
        try:
            logger.info("Running medium model inference")
            logger.debug(f"Input: {input_data[:100]}...")

            if not input_data:
                raise InvalidInputError("Input data cannot be empty")
            if not isinstance(input_data, str):
                raise InvalidInputError(
                    f"Input must be a string, got {type(input_data).__name__}"
                )
            if not self.is_loaded:
                raise RuntimeError("Model not loaded. Call load_model() first.")

            result = f"[MEDIUM] Processed: {input_data}"
            logger.debug(f"Output: {result[:100]}...")
            logger.info(" Inference completed successfully")
            return result

        except (InvalidInputError, RuntimeError):
            raise
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise RuntimeError(f"Medium model inference failed: {e}") from e

    def unload_model(self) -> None:
        """Unload the model and free resources."""
        try:
            logger.info("Unloading medium model...")
            if self.is_loaded:
                self.model = None
                self.is_loaded = False
                logger.info(" Medium model unloaded successfully")
            else:
                logger.debug("Model was not loaded, nothing to unload")
        except Exception as e:
            logger.warning(f"Error during model unloading: {e}")

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the medium model."""
        return {
            'name': 'Medium Model',
            'type': 'medium',
            'version': '1.0.0',
            'description': 'Medium model for balanced performance',
            'model_file': str(self.model_path),
            'is_loaded': self.is_loaded,
            'framework': 'dummy',
            'estimated_memory_mb': 150,
        }
