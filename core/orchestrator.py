"""
Orchestrator module for the AI plugin pipeline.

This module coordinates resource monitoring, plugin selection, model loading,
and inference execution. It demonstrates the Orchestrator design pattern and
proper error handling for educational purposes.
"""
from typing import Any, Optional

from core.resource_selector import select_model_type
from core.plugin_manager import load_plugin, unload_plugin
from core.exceptions import PluginError, ModelLoadError, InvalidInputError
from utils.logger import get_logger
from interfaces.plugin_interface import PluginInterface

logger = get_logger(__name__)


def run_pipeline(
    input_data: str,
    model_override: Optional[str] = None
) -> Any:
    """
    Execute the AI plugin pipeline with resource-aware model selection.

    This is the main orchestration function that:
    1. Validates input data
    2. Selects the most suitable model based on system resources (or uses override)
    3. Loads the appropriate plugin
    4. Loads the model
    5. Executes inference
    6. Cleans up resources

    The function demonstrates best practices for:
    - Input validation
    - Error handling with specific exceptions
    - Resource cleanup using try/finally
    - Comprehensive logging

    Args:
        input_data: The input data to process. Must be a non-empty string.
        model_override: Optional model type to use instead of auto-selection.
                       Must be one of "light", "medium", or "heavy".

    Returns:
        The output from the selected AI model. Type depends on the specific
        plugin implementation.

    Raises:
        InvalidInputError: If input_data is invalid (None, empty, or wrong type)
        PluginError: If no suitable plugin can be loaded
        ModelLoadError: If model loading fails

    Example:
        >>> result = run_pipeline("Hello world")
        >>> print(result)

        >>> # With model override
        >>> result = run_pipeline("Hello world", model_override="heavy")
    """
    plugin: Optional[PluginInterface] = None

    try:
        # Step 1: Validate input
        logger.debug("Validating input data")
        if not input_data:
            raise InvalidInputError("input_data cannot be None or empty")
        if not isinstance(input_data, str):
            raise InvalidInputError(
                f"input_data must be a string, got {type(input_data).__name__}"
            )

        # Step 2: Select model type
        if model_override:
            logger.info(f"Using model override: {model_override}")
            model_type = model_override

            # Validate override value
            valid_types = ["light", "medium", "heavy"]
            if model_type not in valid_types:
                raise InvalidInputError(
                    f"Invalid model_override '{model_type}'. "
                    f"Must be one of: {', '.join(valid_types)}"
                )
        else:
            logger.info("Selecting model based on system resources")
            model_type = select_model_type()

        logger.info(f"Selected model type: {model_type}")

        # Step 3: Load plugin
        try:
            logger.debug(f"Loading plugin: {model_type}")
            plugin = load_plugin(model_type)
            logger.info(f"Plugin loaded: {type(plugin).__name__}")
        except Exception as e:
            logger.error(f"Failed to load plugin '{model_type}': {e}")
            raise PluginError(f"Plugin loading failed: {e}") from e

        # Step 4: Load model
        try:
            logger.debug("Loading model weights")
            plugin.load_model()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            raise ModelLoadError(f"Failed to load model: {e}") from e

        # Step 5: Run inference
        logger.info("Running inference")
        logger.debug(f"Input: {input_data[:50]}...")  # Log first 50 chars
        result = plugin.run(input_data)
        logger.info("Inference completed successfully")
        logger.debug(f"Output: {str(result)[:50]}...")  # Log first 50 chars

        return result

    except (InvalidInputError, PluginError, ModelLoadError):
        # Re-raise our custom exceptions
        raise

    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception("Unexpected error in pipeline execution")
        raise PluginError(f"Pipeline execution failed: {e}") from e

    finally:
        # Step 6: Cleanup - always runs, even if there was an error
        if plugin is not None:
            try:
                logger.debug("Cleaning up plugin resources")
                unload_plugin(plugin)
                logger.debug("Plugin unloaded successfully")
            except Exception as e:
                # Log but don't raise - we don't want cleanup errors
                # to mask the original error
                logger.warning(f"Failed to unload plugin: {e}")
