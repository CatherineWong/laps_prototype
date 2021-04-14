"""
experiment_data | Author : Catherine Wong
Base class for handling and logging Experiment Data objects.
Maintains a registry that can be used to integrate diverse kinds of 'data'.
"""

from class_registry import ClassRegistry

class ExperimentDataStore():
    """ExperimentData: base class for handling all of an experiments ExperimentDatasets
    """
    def __init__(self):
        self._datasets = [] 
    
    def add_dataset(dataset):
        """Adds a dataset to the internal dataset managers."""
        pass

# Global registry. Use ExperimentDatasetRegistry.register(KEY) to create new datasets.
ExperimentDatasetRegistry = ClassRegistry()
class ExperimentDataset():
    """ExperimentDataset: base class for managing many different kinds of ExperimentData.
    Concrete datasets need to be registered using the ExperimentDatasetRegistry decorator.
    """
    def __init__(self, dataset_type=None, dataset_id=None):
        assert dataset_type is not None
        self.dataset_type = dataset_type # Tag for what 'kind' of data it is
        self.dataset_id = None # Dataset handlers should create an ID
        self._dataset_by_id = {}
    
    def add(self, datum):
        assert datum.dataset_type == self.dataset_type or datum.dataset_type is None
        datum.dataset_type = self.dataset_type
        self._dataset_by_id[datum.main_id] = datum
    
    def get_by_id(self, main_id):
        return self._dataset_by_id[main_id]
    
    def checkpoint(self, checkpoint_dir):
        # Run a model specific checkpointing function.
        pass

class ExperimentDatum():
    """ExperimentDatum: Base class for instances of experiment data."""
    def __init__(self, main_id=None, sub_id=None, dataset_type=None, datum_tags=[], data=None):
        self.main_id = main_id # Identifier that can be used to look up the data in the dataset
        self.sub_id = sub_id
        self.dataset_type = dataset_type # What kind of data it is.
        self.datum_tags = datum_tags # Additional tags that can be used to retrieve the data.
        self.data = data
    
    def get(self):
        return self.data
    