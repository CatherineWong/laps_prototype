"""
test_experiment_model | Author : Catherine Wong
Tests for handling models.
"""
import logging
import numpy as np
from src.configlib import constants as C
import src.experimentlib.experiment_models as experiment_models


def dummy_loss_fn(x):
    return np.sum(x)
    
TEST_MODEL = "test_model"
@experiment_models.ExperimentModelRegistry.register(TEST_MODEL)
class TestModel(experiment_models.ExperimentModel):
    def __init__(self, id=TEST_MODEL, state=None):
        super().__init__(id=id, state=None)
        self.data = []
        self.loss = 0
    
    def update(self, data={}, state=None):
        """Naive update function. Memorizes values."""
        self.data = []
        for data_dict in data:
            dataset = state.experiment_data.get_by_id(data_dict[C.ID])
            dataset_ids = dataset.batch if data_dict.get(C.BATCH, False) else dataset.ordering
            self.data += [dataset.get_by_id(id).data for id in dataset_ids]
        
    def evaluate_loss(self, data=[], state=None):
        """Naive loss function. Data is a list of objects including IDs.
         Runs a dummy function on values."""
        loss_data = []
        for data_dict in data:
            dataset = state.experiment_data.get_by_id(data_dict[C.ID])
            dataset_ids = dataset.batch if data_dict.get(C.BATCH, False) else dataset.ordering
            loss_data += [dataset.get_by_id(id).data for id in dataset_ids]
            self.loss = dummy_loss_fn(loss_data)
            
    def checkpoint(self, state=None):
        logging.getLogger().info("[Checkpoint model]")
        logging.getLogger().info(f"\tid: {self.id}")
        logging.getLogger().info(f"\tdata: {self.data}")
        logging.getLogger().info(f"\tloss: {self.loss}")
    
def test_register_new_model():
    new_model = experiment_models.ExperimentModelRegistry.get(TEST_MODEL)
    assert new_model.id == TEST_MODEL