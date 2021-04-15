"""
test_language_data | Author : Catherine Wong
Tests for handling language datasets in experiments.
"""
import src.configlib.constants as C
from src.languagelib.language_data import *
from src.experimentlib.experiment_runner import ExperimentRunner

DEFAULT_CONFIG_FILENAME = "configs/example_language.yaml"
LANGUAGE_DATASET_TAG = JSON_LANGUAGE_DATASET
LOGO_LANGUAGE_DIR = "data/logo/language/logo_unlimited_200/synthetic/train"

def test_initialize_from_config():
    runner = ExperimentRunner(config_filename=DEFAULT_CONFIG_FILENAME)
    runner._init_experiment_data()
    
    assert len(runner.experiment_state.experiment_data._datasets_by_id) == 2
    train_dataset = runner.experiment_state.experiment_data.get_by_id(C.TRAIN)
    assert train_dataset.id == C.TRAIN
    assert train_dataset.dataset_type == C.DATASET_TYPE_LANGUAGE
    assert train_dataset.size() > 0
    assert train_dataset.vocab is not None
    for data_id in train_dataset._datums_by_id:
        assert type(train_dataset._datums_by_id[data_id].data) == type([])
        assert len(train_dataset._datums_by_id[data_id].data) > 0