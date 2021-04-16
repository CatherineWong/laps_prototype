
# Task Learning Library
This repository contains a library with a basic starting framework for running task-based learning experiments. It is especially well-suited for program learning models.
It is currently under development; this file also tracks outstanding implementational features.

## Running and Configuring Experiments
To run an experiment with this library, you need two basic ingredients:
1. A `config` file that determines all of the experimental parameters.
2. An executable `.py` file that launches an experiment from the config.

### Configuration Files
To configure all experimental parameters, you will need a `config` file with these basic parts. See `configs\example_config.yaml` for an example.
1. `metadata`: all experimental metadata that should persist across every iteration and should be accessible to all experimental blocks in each iteration.
2. `data`: all experimental data maintained throughout the experiment. This includes datasets, but also is a writable store of data that models can access during an experiment.
3. `models`: all models that need to be initialized for the experiment. Models control the experimental functions that will be called to actually run an experiment.
4. `experiment`: all experimental blocks that will be iterated over at each iteration. This calls task datasets (which can update based on the iteration) or models that can mutate and access the experimental data.
Together, these configuration parameters configure and fully define a runnable experiment.

## Experiments
Experiments use the configuration file to initialize and manage the experiments. These configure the following parts of the experiment.

### Experiment Initialization
Experiments are initialized, managed, and run by an `ExperimentRunner`, which maintains a global `ExperimentState` throughout the experiment. 
Initializing the experiment:
1. Initializes and configures the metadata. This sets up the persistent global parameters including the checkpoint directory and logger.
2. Initializes and configures the data. This loads all of the initial datasets or data types specified by the config.
3. Initializes and configures the models. This initializes all of the models defined by the config.

When initializing the `ExperimentMetadata` at the start of the experiment, the experiment will configure the following useful globally accessible functionalities:
1. Checkpoint directory. All models and data should be able to checkpoint to a global checkpoint directory. This creates a timestamped checkpoint directory under `checkpoint_dir`.
2. Logging file. All models and data should be able to log to a global log file. This creates a common logfile under `log_dir` and configures the global Python logger to output to both the IO stream and to the file. We use the Python `logging` library; `logging.getLogger` will now write out to both.

> dev: all experiment running functionality is located in `src/experimentlib`.
> 
> dev: all tests use pytest. Exampple: `python -m pytest tests/experimentlib/test_experiment_runner.py`

### Experiment Data
Experiment data of any kind (tasks, language annotations, synthesized programs) are `ExperimentDataset`s. 
The Experiment maintains an `ExperimentData` collection of all of its `ExperimentDataset`s, which can be accessed by any experimental block.
Creating a new dataset that can be loaded from the config requires:
1. Implementing a subclass of `ExperimentDataset`.
2. Registering the experiment dataset to the global `ExperimentDataRegistry` in `experimentlib\experiment_data`. This allows the experiment runner to import the experiments from the store. See the test for an example.

> dev: the base dataset functionality is located in `src/experimentlib/experiment_data.py`. However, specific kinds of datasets are managed by specific libraries based on their data type, such as `languagelib` and `programlib`.

6. [TODO] Finally, store a cut of DreamCoder (with the binaries accessible) as a library fork, ideally with OCaml executables. Implement programlib to unwrap / wrap out the various program components. Verify task loading (of image tasks); and programs from the frontiers (just load the programs as frontiers or ground truth annotations -- we can write them out as a different kind of taskv or separate from the frontiers.)

### Experiment Models
Experiment models of any kind (generative, discriminative) are derived from the ExperimentModel class.

TODO: create a dummy model and verify registry, initialization, data access, and checkpointing with the language data.
Write very silly no train and sampling functions. 

### Experiment
Experiments iterate over a series of function calls to either the ExperimentDataset or ExperimentModel.




