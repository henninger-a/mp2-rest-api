# data_loaders.py
from pathlib import Path

import logging
import pandas as pd
import json
import yaml


# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame.
    filepath is a Path object.
    """
    df = pd.read_csv(filepath)
    logger.info(f'Loaded CSV file: {filepath} ({len(df)} rows)')
    return df


def load_json(filepath):
    """Load a JSON file into a Python object (dict or list).
    filepath is a Path object.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    logger.info(f'Loaded JSON file: {filepath}')
    return data


def load_yaml(filepath):
    """Load a YAML file into a Python object.
    filepath is a Path object.
    """
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)
    logger.info(f'Loaded YAML file: {filepath}')
    return config


def load_data(filepath):
    """Load a file based on its extension.
    filepath is a string, such as 'fixtures/sample.csv'
    """
    path = Path(filepath)
    if path.suffix == '.csv':
        return load_csv(path)
    elif path.suffix == '.json':
        return load_json(path)
    elif path.suffix == '.yaml':
        return load_yaml(path)
    else:
        logger.error(f'Unsupported file format: {path.suffix}')
        raise ValueError
