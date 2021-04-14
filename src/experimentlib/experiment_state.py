"""
experiment_state.py | Author : Catherine Wong

Global experiment state objects maintained throughout an experiment.
"""
import os
import random
import logging
import src.utilslib.utils as utils
from src.configlib import constants as C
from src.experimentlib.experiment_data import ExperimentData
from src.experimentlib.experiment_models import ExperimentModels

class ExperimentState():
    def __init__(self):
        self.metadata = ExperimentMetadata()
        self.experiment_data = ExperimentData()
        self.experiment_models = ExperimentModels()

class ExperimentMetadata():
    """ExperimentMetadata: maintains global experiment running metadata.
    Expects initialization from a config.
    Accessible but should not be specific to Data or Models."""
    def __init__(self):
        self.experiment_id = None
        self.seed = None # Random seed
        self.iteration = 0 # What iteration we are on
        self.end_iteration = 0
        
        self.timestamp = utils.escaped_timestamp()
        self.new_timestamped_log = False # If true: creates new log
        self.new_timestamped_checkpoint_dir = False # If true: creates new dir
        self.log_dir = None
        self.log_file = None # If not none: writes log file here
        self.checkpoint_dir = None # If not none: writes checkpoints here
    
        self.debug = False # Top-level debug flag.
        self.logging_verbosity = logging.INFO # Logging verbosity.
        
    def init_from_config(self, config):
        """Initializes attributes directly from a config file.
        Creates timestamped log and checkpoints if specified by the config.
        """
        assert C.EXPERIMENT_METADATA in config
        metadata_config = config[C.EXPERIMENT_METADATA]
        for k, v in metadata_config.items():
            if k not in dir(self):
                print(f"Unknown attribute: {k}")
                assert False
            setattr(self, k, v)
        assert self.experiment_id is not None
        assert self.end_iteration >= self.iteration
        self._init_timestamped_checkpoint_and_logfile()
        self._init_logger()
    
    def _init_timestamped_checkpoint_and_logfile(self):
        """Initializes checkpoint and log files."""
        timestamped_experiment_base = f"{self.experiment_id}_{self.timestamp}"
        if self.new_timestamped_checkpoint_dir:
            assert self.checkpoint_dir is not None
            self.checkpoint_dir = os.path.join(self.checkpoint_dir, timestamped_experiment_base)
            utils.mkdir_if_necessary(self.checkpoint_dir)
        if self.new_timestamped_log:
            assert self.log_dir is not None
            self.log_file = os.path.join(self.log_dir, timestamped_experiment_base + C.LOG_POSTFIX)
    
    def _init_logger(self):
        """Basic logger configuration. Logs to file and out."""
        logging.basicConfig(level=self.logging_verbosity)
        logger = logging.getLogger()
        if self.log_file is not None:
            logfile_handler = logging.FileHandler(self.log_file)
            logger.addHandler(logfile_handler)
            logger.setLevel(self.logging_verbosity)
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
        logger.setLevel(self.logging_verbosity)
    
    def _init_random_seed(self):
        if self.seed is not None:
            random.seed(self.seed)
    
    def log(self):
        # Prints information about the config.
        logging.getLogger().info("[Metadata config]")
        logging.getLogger().info(f"\texperiment_id: {self.experiment_id}")
        logging.getLogger().info(f"\tcheckpoint_dir: {self.checkpoint_dir}")
        logging.getLogger().info(f"\tlog_file: {self.log_file}")
        logging.getLogger().info(f"\tseed: {self.seed}")
        logging.getLogger().info(f"\titeration: {self.iteration}")
        logging.getLogger().info(f"\tend_iteration: {self.end_iteration}")
        