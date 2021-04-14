"""
experiment_models | Author : Catherine Wong.
Base class for handling Experiment Model objects.
Maintains a registry that can be used to integrate diverse 'models'.
"""
from class_registry import ClassRegistry

class ExperimentModels():
    """ExperimentModels: a collection of all of the experiment models for a given experiment."""
    def __init__(self):
        self._models_by_id = {}
    
    def add_model(self, model):
        """Adds a model to the internal model manager."""
        self._models_by_id[model.id] = model
    
    def get_by_id(self, id):
        return self._models_by_id[id]
    
    def checkpoint_all(self):
        for dataset_id in self._datasets_by_id:
            self._datasets_by_id[dataset_id].checkpoint()

# Global registry. Use ExperimentModelRegistry.register(KEY) to create new datasets.
ExperimentModelRegistry = ClassRegistry()

class ExperimentModel():
    """ExperimentModel: base class for managing any kind of model. Concrete models need to be registered using the ExperimentModelRegistry decorator.
    
    Model functions that take a `state` arg will be given the experiment state, from which they can use any necessary data.
    """
    def __init__(self, id=None, state=None):
        assert id is not None
        self.id = id
    
    def checkpoint(self, checkpoint_dir):
        # Run a model specific checkpointing function.
        raise RuntimeError('Not implemented: checkpointing function.')