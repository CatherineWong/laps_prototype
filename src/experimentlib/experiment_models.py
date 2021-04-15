"""
experiment_models | Author : Catherine Wong.
Base class for handling Experiment Model objects.
Maintains a registry that can be used to integrate diverse 'models'.
"""

from class_registry import ClassRegistry
from src.configlib import constants as C

class ExperimentModels():
    """ExperimentModels: a collection of all of the experiment models for a given experiment."""
    def __init__(self):
        self._models_by_id = {}
    
    def add_model(self, model):
        """Adds a model to the internal model manager."""
        self._models_by_id[model.id] = model
    
    def get_by_id(self, id):
        return self._models_by_id[id]
    
    def checkpoint(self, to_checkpoint, state):
        """to_checkpoint: array of IDs to checkpoint.
            state: experiment_state
        """
        for id in self._models_by_id:
            if id in to_checkpoint or C.ALL in to_checkpoint:
                self._models_by_id[id].checkpoint(state)

# Global registry. Use ExperimentModelRegistry.register(KEY) to create new datasets.
ExperimentModelRegistry = ClassRegistry()

class ExperimentModel():
    """ExperimentModel: base class for managing any kind of model. Concrete models need to be registered using the ExperimentModelRegistry decorator.
    
    Model functions that take a `state` arg will be given the experiment state, from which they can use any necessary data.
    """
    def __init__(self, id=None, state=None):
        assert id is not None
        self.id = id
    
    def checkpoint(self, state=None):
        # Run a model specific checkpointing function.
        raise RuntimeError('Not implemented: checkpointing function.')