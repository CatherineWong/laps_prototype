"""
experiment_state.py | Author : Catherine Wong

Global experiment state object maintained throughout an experiment.
"""
class ExperimentState():
    def __init__(self):
        self.metadata = ExperimentMetadata()
        self.experiment_data = None
        self.experiment_models = [] # Array of models maintained by this experiment.

class ExperimentMetadata():
    def _init__(self):
        self.config_tag = "metadata"
        self.experiment_name = None
        self.seed = 0 # Random seed
        self.iteration = 0 # What iteration we are on
        self.end_iteration = 0
        
        self.checkpoint_results = False
        self.result_dir = None # Top-level checkpoint dir
        self.debug = False # Top-level debug flag.
        self.logging_verbosity = 0 # Logging verbosity.
    
    def init_from_config(self, config):
        # Inits from a config and checks that we have set the appropriate parameters.
        assert self.config_tag in config
        metadata_config = config[CONFIG_TAG]
        for k, v in metadata_config.items():
            setattr(self, k, v)
        assert self.experiment_name is not None
        assert self.end_iteration >= self.iteration
    
    def log(self):
        # Prints information about the config.
        if self.logging_verbosity > 0:
            print("Metadata:")
            print(f"\texperiment_name: {self.experiment_name}")
            print(f"\tresult_dir: {self.experiment_name}")
        