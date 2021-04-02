"""
test_experiment_runner.py | Author : Catherine Wong

Test for the experiment runner class which initializes experiments from a config and runs them.

From root:
python -m pytest tests/test_experiment_runner.py
"""
from src.experimentlib.experiment_runner import ExperimentRunner

DEFAULT_CONFIG_FILENAME = "configs/example_config.yaml"

def test_init_experiment_metadata():
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner._init_experiment_metadata()
    metadata = runner.experiment_state.metadata
    
    # Check the attributes were set from the file
    assert metadata.experiment_name == "test_experiment"