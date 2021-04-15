"""
main.py | Author : Catherine Wong

Demo general purpose entrypoint for running model-based experiments.
Data should be defined in the data directory.
Experiments should be defined via config files.
Main needs to import any models and data for the registry.
"""
from src.experimentlib.experiment_runner import ExperimentRunner

# Main-specific models and data handlers.
from tests.experimentlib.test_experiment_data import *
from tests.experimentlib.test_experiment_models import *

if __name__ == '__main__':
    runner = ExperimentRunner(config_filename="configs/example_config.yaml")
    runner.init_experiment()
    for iter_idx in range(runner.experiment_state.metadata.end_iteration):
        runner.run_iteration()