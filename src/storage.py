import logging
from .models import DatasetInfo

logger = logging.getLogger(__name__)


class DatasetStorage:
    def __init__(self):
        self._store = {}
        self._counter = 0

    def save(self, df, filename):
        """Store a copy of the data and return a new integer ID."""
        self._counter += 1
        dataset_id = self._counter
        self._store[dataset_id] = {'Filename': filename, 'Data': df.copy()}
        logger.debug(f'Saved dataset with an id of {dataset_id}')
        return dataset_id

    def get(self, dataset_id):
        """Return a copy of the stored DataFrame, or None."""
        item = self._store.get(dataset_id)
        if item is None:
            logger.debug(f'Dataset with id {dataset_id} not found')
            return None
        logger.debug(f'Retrieved dataset with id {dataset_id}')
        return item['Data'].copy()

    def get_metadata(self, dataset_id):
        """Return the dataset metadata, or None."""
        dataset = self._store.get(dataset_id)
        logger.debug(f'Retrieved metadata for dataset with id {dataset_id}')
        return DatasetInfo(id = dataset_id, 
                           filename = dataset['Filename'], 
                           rows = dataset['Data'].shape[0], 
                           columns = dataset['Data'].shape[1], 
                           column_names = list(dataset['Data'].columns))

    def update(self, dataset_id, df):
        """Replace an existing dataset; return True, or False if missing."""
        if self._store.get(dataset_id) is None:
            logger.debug(f'No exisiting dataset with id {dataset_id} found')
            return False
        self._store[dataset_id]['Data'] = df.copy()
        logger.debug(f'Exisiting dataset with id {dataset_id} updated')
        return True

    def clear(self):
        """Clear all data and reset the ID counter."""
        self._store.clear()
        self._counter = 0
