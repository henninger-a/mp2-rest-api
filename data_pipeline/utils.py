import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt='%H:%M:%S'
    )


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file() is True:
        logger.info(f"Input file validated: '{filepath}'")
        return True
    else:
        logger.error(f"Input file not fould: '{filepath}'")
        return False