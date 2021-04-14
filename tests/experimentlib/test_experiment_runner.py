"""
test_experiment_runner.py | Author : Catherine Wong

Test for the experiment runner class which initializes experiments from a config and runs them.

From root:
python -m pytest tests/test_experiment_runner.py
"""
import os
import yaml

import src.configlib.constants as C
from src.experimentlib.experiment_runner import ExperimentRunner
from tests.experimentlib.test_experiment_data import *
from tests.experimentlib.test_experiment_models import *

DEFAULT_CONFIG_FILENAME = "configs/example_config.yaml"

def check_dir_exists_and_remove(path):
    assert os.path.exists(path)
    os.rmdir(path)
    
def check_file_exists_and_remove(path):
    assert os.path.exists(path)
    os.remove(path)

def test_init_experiment():
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner.init_experiment()
    assert runner.experiment_state.metadata.iteration == 0
    assert len(runner.experiment_state.experiment_data._datasets_by_id)
    assert len(runner.experiment_state.experiment_models._models_by_id) == 1
    
def test_init_experiment_data_from_config():
    """Test that we can initialize_dummy data from a config."""
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner._init_experiment_data()
    # Assert that the dataset is in there.
    assert len(runner.experiment_state.experiment_data._datasets_by_id) == 1
    dataset_id = TEST_ORDERED_DATASET_TAG
    dataset = runner.experiment_state.experiment_data.get_by_id(TEST_ORDERED_DATASET_TAG)
    assert dataset.id == TEST_ORDERED_DATASET_TAG

def test_init_experiment_models_from_config():
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner._init_experiment_models()
    # Assert that we've initialized a model.
    assert len(runner.experiment_state.experiment_models._models_by_id) == 1
    model = runner.experiment_state.experiment_models.get_by_id(TEST_MODEL)
    assert model.id == TEST_MODEL

def test_init_experiment_metadata_from_config():
    """Test that we can initialize metadata from a config file"""
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner._init_experiment_metadata()
    metadata = runner.experiment_state.metadata
    
    timestampeable_attributes = [
        'checkpoint_dir', 'log_file'
    ]
    # Check the attributes were set from the file
    f = open(DEFAULT_CONFIG_FILENAME, 'r')
    config = yaml.load(f, Loader=yaml.Loader)
    metadata_config = config[C.EXPERIMENT_METADATA]
    for (k, v) in metadata_config.items():
        if k not in timestampeable_attributes:
            assert getattr(metadata, k) == v
    # Assert that we created a timestamped logfile and checkpoint
    for k in timestampeable_attributes:
        timestamped_experiment_base = f"{metadata.experiment_id}_{metadata.timestamp}"
        assert timestamped_experiment_base in getattr(metadata, k) 
    # Check that we have a checkpoint and then clean it up.
    check_dir_exists_and_remove(metadata.checkpoint_dir)
    # Check that we have a logfile and then clean it up
    check_file_exists_and_remove(metadata.log_file)

def test_run_iteration():
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner.init_experiment()
    runner.run_iteration()
    assert runner.experiment_state.metadata.iteration == 1
    
    # Test that we got a batch of data
    dataset =  runner.experiment_state.experiment_data.get_by_id(TEST_ORDERED_DATASET_TAG)
    assert dataset.batch is not None
    assert dataset.batch == list(range(10))