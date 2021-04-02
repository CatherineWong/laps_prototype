"""
experiment_runner | Author : Catherine Wong

Initializes and runs time-stamped experiments.
Expects a config file.
"""
import yaml
from src.experimentlib.experiment_state import ExperimentState

class ExperimentRunner():
    """Top-level class for running experiments.
    Initialized from a YAML config file.
    Initializes and maintains an ExperimentState.
    Running the experiment iterates through the experiment blocks.
    """
    def __init__(self, config_filename):
        self.config = self._load_config(config_filename)
        self.experiment_state = ExperimentState()
    
    def _load_config(self, config_filename):
        # Loads a config file and sets the internal config object.
        f = open(config_filename, 'r')
        return yaml.load(f, Loader=yaml.Loader)
        
    def init_experiment(self):
        # Initializes an experiment.
        self._init_experiment_metadata()
        # Initializes all of the data.
        # Initializes all of the models.
        # Initializes the top-level scheduler.
        pass
    
    def _init_experiment_metadata(self):
        """Initializes the experiment metadata."""
        self.experiment_state.metadata.init_from_config(self.config)
        # Create a top-level experiment directory based on the config experiment name
        self.experiment_state.metadata.log()
        
    def _init_experiment_data(self):
        # Initializes the experiment data.
        pass
    
    def _init_experiment_models(self):
        # Initializes the experiment models in the YAML file by passing them the config.
        pass
    
    def run_iteration(self):
        # Runs an iteration of the experiment.
        pass