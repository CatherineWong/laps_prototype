"""
language_dataset.py | Author : Catherine Wong
"""
import os, json
import src.experimentlib.experiment_data as experiment_data
import src.configlib.constants as C

@experiment_data.ExperimentDatasetRegistry.register("laps_language")
class LAPSLanguageDataset(experiment_data.ExperimentDataset):
    """LAPSLanguageDatasets: utility function to load language datasets.
    Contains LAPSLanguageDatum
    Expects a set of train and test data in the dataset.
    Maintains a global vocabulary and a train and test vocabulary.
    """
    DEFAULT_LANGUAGE_FILE = "language.json"
    DEFAULT_VOCAB_FILE = "vocab_file.json"
    def __init__(self,
                domain=None,
                task_set=None,
                data_dirs=None,
                base_language_file=DEFAULT_LANGUAGE_FILE,
                base_vocab_file=DEFAULT_VOCAB_FILE):
        self.dataset_type = C.DATATYPE_LANGUAGE
        self.domain = domain
        self.task_set = task_set
        self._load_language_for_data_dirs(data_dirs, base_language_file, base_vocab_file)
        self.vocabs = {
            C.ALL : set(),
            C.TRAIN : set(),
            C.TEST : set()
        }
    
    def _load_language_for_data_dirs(self, data_dirs, base_language_file, base_vocab_file):
        for data_dir in data_dirs:
            for split in [C.TRAIN, C.TEST]:
                language_file = os.path.join(data_dir, split, base_language_file)
                assert os.path.exists(language_file)
                with open(language_file) as f:
                    language_data = 
            
    def checkpoint(self):
        pass
            
class LAPSLanguageDatum(experiment_data.ExperimentDatum):
    def __init__(self, **kwargs):
        super__init__(self, **kwargs)
        