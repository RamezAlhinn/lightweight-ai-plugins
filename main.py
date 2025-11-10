"""
Main entry point for the Lightweight AI Plugin Framework.

This module initializes the resource-aware AI pipeline and processes input data
using the most suitable model based on system resources.
"""
import argparse
import logging
import sys
from typing import Optional

from core.orchestrator import run_pipeline
from core.exceptions import PluginError
from utils.logger import setup_logging, get_logger

logger = get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed command-line arguments

    Example:
        >>> args = parse_arguments()
        >>> print(args.input_data)
    """
    parser = argparse.ArgumentParser(
        description="Lightweight AI Plugin Framework - Resource-aware AI model execution",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "input_data",
        nargs="?",
        default="Hello from main",
        type=str,
        help="Input data to process through the AI model"
    )
    parser.add_argument(
        "--model",
        choices=["light", "medium", "heavy"],
        default=None,
        help="Override automatic model selection with a specific model type"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging verbosity level"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Optional file path to write logs to"
    )
    return parser.parse_args()


def main() -> int:
    """
    Main execution function.

    This function:
    1. Parses command-line arguments
    2. Sets up logging
    3. Runs the AI pipeline
    4. Handles errors gracefully

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_arguments()

    # Setup logging
    log_level = getattr(logging, args.log_level)
    setup_logging(level=log_level, log_file=args.log_file)

    try:
        logger.info("=" * 60)
        logger.info("Lightweight AI Plugin Framework - Starting")
        logger.info("=" * 60)
        logger.info(f"Input data: {args.input_data}")

        if args.model:
            logger.info(f"Model override: {args.model}")

        # Run the pipeline
        result = run_pipeline(args.input_data, model_override=args.model)

        logger.info(f"Pipeline completed successfully")
        logger.info(f"Result: {result}")
        print(f"\n✓ Result: {result}\n")
        return 0

    except PluginError as e:
        logger.error(f"Plugin error: {e}", exc_info=True)
        print(f"\n✗ Error: {e}\n", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        logger.warning("Execution interrupted by user")
        print("\n\n✗ Interrupted by user\n", file=sys.stderr)
        return 1

    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"\n✗ Unexpected error: {e}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
