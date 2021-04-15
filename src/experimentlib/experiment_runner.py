"""
experiment_runner | Author : Catherine Wong

Initializes and runs time-stamped Experiments. 
ExperimentRunner maintains and updates an ExperimentState.
Expects a config file.
"""
import logging
import yaml
from src.configlib import constants as C
from src.experimentlib.experiment_state import ExperimentState
from src.experimentlib.experiment_data import ExperimentDatasetRegistry
from src.experimentlib.experiment_models import ExperimentModelRegistry

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
        """Loads a YAML config file and sets the internal config object."""
        f = open(config_filename, 'r')
        return yaml.load(f, Loader=yaml.Loader)
        
    def init_experiment(self):
        """Initializes an ExperimentState."""
        self._init_experiment_metadata()
        # Initializes all of the data.
        self._init_experiment_data()
        # Initializes all of the models.
        self._init_experiment_models()
    
    def _init_experiment_metadata(self):
        """Initializes the experiment metadata from the config."""
        self.experiment_state.metadata.init_from_config(self.config)        
        self.experiment_state.metadata.log()
        
    def _init_experiment_data(self):
        # Initializes the experiment data.
        assert C.EXPERIMENT_DATA in self.config
        data_config = self.config[C.EXPERIMENT_DATA]
        for dataset_config in data_config:
            assert C.HANDLER in dataset_config
            assert C.PARAMS in dataset_config
            handler, params = dataset_config[C.HANDLER], dataset_config[C.PARAMS]
            dataset =  ExperimentDatasetRegistry.get(handler, **params)
            self.experiment_state.experiment_data.add_dataset(dataset)
    
    def _init_experiment_models(self):
        # Initializes the experiment models in the YAML file by passing them the config. Passes in the current experimental state.
        assert C.EXPERIMENT_MODELS in self.config
        models_config = self.config[C.EXPERIMENT_MODELS]
        for model_config in models_config:
            assert C.HANDLER in model_config
            assert C.PARAMS in model_config
            handler, params = model_config[C.HANDLER], model_config[C.PARAMS]
            model = ExperimentModelRegistry.get(handler, state=self.experiment_state, **params)
            self.experiment_state.experiment_models.add_model(model)
    
    def run_iteration(self):
        # Runs an iteration of the experiment.
        assert C.EXPERIMENT in self.config
        experiment_blocks = self.config[C.EXPERIMENT]
        for block in experiment_blocks:
            if C.EXPERIMENT_DATA in block:
                # Run a function on the experiment data.
                dataset_id = block[C.EXPERIMENT_DATA]
                dataset = self.experiment_state.experiment_data.get_by_id(dataset_id)
                dataset_fn = getattr(dataset, block[C.FN])
                dataset_fn(**block[C.PARAMS])
            elif C.EXPERIMENT_MODELS in block:
                # Run a model function.
                model_id = block[C.EXPERIMENT_MODELS]
                model = self.experiment_state.experiment_models.get_by_id(model_id)
                model_fn = getattr(model, block[C.FN])
                model_fn(state=self.experiment_state, **block[C.PARAMS])
            elif C.CHECKPOINT in block:
                checkpoint_block =  block[C.CHECKPOINT]
                if C.EXPERIMENT_METADATA in checkpoint_block:
                    self.experiment_state.metadata.checkpoint(checkpoint_block[C.EXPERIMENT_METADATA], self.experiment_state)
                if C.EXPERIMENT_DATA in checkpoint_block:
                    self.experiment_state.experiment_data.checkpoint(checkpoint_block[C.EXPERIMENT_DATA], self.experiment_state)
                if C.EXPERIMENT_MODELS in checkpoint_block:
                    self.experiment_state.experiment_models.checkpoint(checkpoint_block[C.EXPERIMENT_MODELS], self.experiment_state)
                    
            else:
                raise RuntimeError('Unknown experiment block type.')
        
        self.experiment_state.metadata.iteration += 1