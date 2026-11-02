# src/data_output.py
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_data(df, filepath):
    """Save a DataFrame as a CSV file."""
    output = Path(filepath)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index = False)
    logger.debug(f'Rows Saved: {len(df)}, Output Path: {output}')
    return output
