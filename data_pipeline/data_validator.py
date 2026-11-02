# src/data_validator.py
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    original = df
    for column in required_columns:
        if column not in df.columns:
            print(f'{column} not in df')
            raise ValueError
        
    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    invalid_rows.append(i)
        logger.warning(f'Removed {len(invalid_rows)} row(s) from {col} with invalid numerical values')

        df = df.drop(index=invalid_rows)
        df[col] = pd.to_numeric(df[col])
    logger.debug(f'Valid Rows: {len(df)}, Rows Removed: {len(original) - len(df)}')
    return df
