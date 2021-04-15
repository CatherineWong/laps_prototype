"""
experiment_data | Author : Catherine Wong
Base class for handling and logging Experiment Data objects.
Maintains a registry that can be used to integrate diverse kinds of 'data'.
"""
import random
from collections import defaultdict
from class_registry import ClassRegistry
from src.configlib import constants as C

class ExperimentData():
    """ExperimentData: a collection of all of the experiment datasets for a given experiment.
    """
    def __init__(self):
        self._datasets_by_id = {}
    
    def add_dataset(self, dataset):
        """Adds a dataset to the internal dataset managers."""
        self._datasets_by_id[dataset.id] = dataset
    
    def get_by_id(self, id):
        return self._datasets_by_id[id]
    
    def checkpoint(self, to_checkpoint, state):
        """to_checkpoint: array of IDs to checkpoint.
            state: experiment_state
        """
        for id in self._datasets_by_id:
            if id in to_checkpoint or C.ALL in to_checkpoint:
                self._datasets_by_id[id].checkpoint(state)

# Global registry. Use ExperimentDatasetRegistry.register(KEY) to create new datasets.
ExperimentDatasetRegistry = ClassRegistry()
class ExperimentDataset():
    """ExperimentDataset: base class for managing many different kinds of ExperimentData.
    Datums maintain an array of [tags]: strings that can be used to order and slice specific sets of data.
    Concrete datasets need to be registered using the ExperimentDatasetRegistry decorator.
    """
    def __init__(self, id=None, dataset_type=None):
        assert dataset_type is not None
        assert id is not None
        self.id = id 
        self.dataset_type = dataset_type # Tag for what 'kind' of data it is
        
        self._datums_by_id = {} 
        
        self.ordering = None
        self.pointer = 0
        self.epoch = 0
        self.batch = None
    
    def checkpoint(self, state=None):
        # Run a model specific checkpointing function. Will be passed the model state.
        raise RuntimeError('Not implemented: checkpointing function.')
    
    def size(self):
        return len(self._datums_by_id)
    
    def get_by_id(self, datum_id):
        return self._datums_by_id[datum_id]
        
    def add(self, datum):
        """Adds a datum. Note that if there is an existing ordering, this will fail, because it is not well defined."""
        assert self.ordering is None
        assert datum.dataset_type == self.dataset_type or datum.dataset_type is None
        datum.dataset_type = self.dataset_type
        self._datums_by_id[datum.id] = datum
    
    def initialize_ordering(self, shuffle=False, from_ordering=None):
        """Initialize ordering over the dataset by IDs.
        """
        if from_ordering:
            self.ordering = from_ordering
        else:
            self.ordering = sorted(list(self._datums_by_id.keys()))
        if shuffle:
            random.shuffle(self.ordering)
        self.pointer = 0
        self.epoch = 0
    
    def get_batch(self, batch_size=None):
        """Gets a batch with wraparound. 
        batch_size: if None, uses entire dataset.
        sets: self.batch to the current batch.
        Returns: [array of datum ids]
        """
        assert self.ordering is not None
        assert batch_size <= len(self.ordering)
        if batch_size is None: batch_size = len(self.ordering)
        
        start = self.pointer
        end = self.pointer+batch_size
        
        batch = self.ordering[start:end]
        if end > len(self.ordering):
            self.epoch += 1
            start = 0
            end = end - len(self.ordering)
            batch += self.ordering[start:end]
        self.pointer = end
        self.batch = batch
        return batch
            
class ExperimentDatum():
    """ExperimentDatum: Base class for instances of experiment data."""
    def __init__(self, id=None, sub_id=None, dataset_type=None, datum_tags=[], data=None):
        self.id = id # Identifier that can be used to look up the data in the dataset
        self.dataset_type = dataset_type # What kind of data it is.
        self.datum_tags = datum_tags # Additional tags that can be used to retrieve the data.
        self.data = data
    
    def get(self):
        return self.data
    