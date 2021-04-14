"""
test_experiment_model | Author : Catherine Wong
Tests for handling models.
"""
import src.experimentlib.experiment_models as experiment_models

TEST_MODEL = "test_model"
@experiment_models.ExperimentModelRegistry.register(TEST_MODEL)
class TestModel(experiment_models.ExperimentModel):
    def __init__(self, id=TEST_MODEL, state=None):
        super().__init__(id=id, state=None)
    def checkpoint():
        pass

def test_register_new_model():
    new_model = experiment_models.ExperimentModelRegistry.get(TEST_MODEL)
    assert new_model.id == TEST_MODEL