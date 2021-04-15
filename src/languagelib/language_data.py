"""
language_dataset.py | Author : Catherine Wong.
Utility functions for loading common language datasets.
"""
import logging
import os, json
import src.experimentlib.experiment_data as experiment_data
import src.configlib.constants as C

JSON_LANGUAGE_DATASET = "json_language_dataset"
@experiment_data.ExperimentDatasetRegistry.register(JSON_LANGUAGE_DATASET)
class JSONLanguageDataset(experiment_data.ExperimentDataset):
    DEFAULT_JSON_LANGUAGE_FILE = "language.json"
    DEFAULT_JSON_VOCAB_FILE = "vocab.json"
    def __init__(self,
                id=None,
                input_dirs=None,
                base_language_file=DEFAULT_JSON_LANGUAGE_FILE,
                base_vocab_file=DEFAULT_JSON_VOCAB_FILE,
                shuffle=False,
                from_ordering=None):
        super().__init__(id=id, dataset_type=C.DATASET_TYPE_LANGUAGE)
        self.input_dirs = input_dirs 
        self.base_language_file = base_language_file
        self.base_vocab_file = base_vocab_file
        
        self.vocab = {}
        
        assert self.input_dirs is not None
        assert self.base_language_file is not None
        assert self.base_vocab_file is not None
        
        self._initialize_from_json()
    
    def _initialize_from_json(self):
        for input_dir in self.input_dirs:
            vocab_file = os.path.join(input_dir, self.base_vocab_file)
            assert os.path.exists(vocab_file)
            with open(vocab_file) as f:
                self.vocab = json.load(f)
                
            language_file = os.path.join(input_dir, self.base_language_file)
            assert os.path.exists(language_file)
            with open(language_file) as f:
                language_dataset = json.load(f)
            for id, data in language_dataset.items():
                new_datum = LanguageDatum(id=id, data=data)
                self.add(new_datum)
                 
    def checkpoint(self, state):
        logging.getLogger().info("[Checkpoint data]")
        logging.getLogger().info(f"\tid: {self.id}")
        logging.getLogger().info(f"\thandler: {JSON_LANGUAGE_DATASET}")
        logging.getLogger().info(f"\tsize: {self.size()}")
        logging.getLogger().info(f"\tvocab_size: {len(self.vocab)}")
            
class LanguageDatum(experiment_data.ExperimentDatum):
    def __init__(self, **kwargs):
        super().__init__(dataset_type=C.DATASET_TYPE_LANGUAGE, **kwargs)
        assert type(self.data) == type([])