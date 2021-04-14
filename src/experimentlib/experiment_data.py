"""
experiment_data | Author : Catherine Wong
Base class for handling and logging Experiment Data objects.
Maintains a registry that can be used to integrate diverse kinds of 'data'.
"""
import random
from class_registry import ClassRegistry

class ExperimentData():
    """ExperimentData: a collection of all of the experiment datasets for a given experiment.
    """
    def __init__(self):
        self._datasets = [] 
        self._datasets_by_id = {}
    
    def add_dataset(dataset):
        """Adds a dataset to the internal dataset managers."""
        pass

# Global registry. Use ExperimentDatasetRegistry.register(KEY) to create new datasets.
ExperimentDatasetRegistry = ClassRegistry()
class ExperimentDataset():
    """ExperimentDataset: base class for managing many different kinds of ExperimentData.
    Concrete datasets need to be registered using the ExperimentDatasetRegistry decorator.
    """
    def __init__(self, dataset_id=None, dataset_type=None):
        assert dataset_type is not None
        assert dataset_id is not None
        self.dataset_id = dataset_id 
        self.dataset_type = dataset_type # Tag for what 'kind' of data it is
        
        self._datums_by_id = {}
        
        self.ordering = None
        self.pointer = 0
        self.epoch = 0
    
    def checkpoint(self, checkpoint_dir):
        # Run a model specific checkpointing function.
        raise RuntimeError('Not implemented: checkpointing function.')
        
    def add(self, datum):
        """Adds a datum. Note that if there is an existing ordering, this will fail, because it is not well defined."""
        assert self.ordering is None
        assert datum.dataset_type == self.dataset_type or datum.dataset_type is None
        datum.dataset_type = self.dataset_type
        self._datums_by_id[datum.id] = datum
    
    def get_by_id(self, datum_id):
        return self._datums_by_id[datum_id]
    
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
        """Gets a batch with wraparound. Increments the epochs if you have wrapped around. Returns a set of IDs in sorted order for the given batch."""
        assert self.ordering is not None
        assert batch_size < len(self.ordering)
        
        start = self.pointer
        end = self.pointer+batch_size
        
        batch = self.ordering[start:end]
        if end > len(self.ordering):
            self.epoch += 1
            start = 0
            end = end - len(self.ordering)
            batch += self.ordering[start:end]
        self.pointer = end
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
    