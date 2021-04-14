
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
1. [TODO] Change experiment name to experimetn name

> dev: all experiment running functionality is located in `src/experimentlib`.
> dev: all tests use pytest. Exampple: `python -m pytest tests/experimentlib/test_experiment_runner.py`
### Experiment Data
Experiment data of any kind (tasks, language annotations, synthesized programs) are derived from the 
1. [TODO] Change data to have a data ID.

### Experiment Models
Experiment models of any kind (generative, discriminative) are derived from the 

### Experiment
Experiments iterate over a series of function calls to either the ExperimentDataset or ExperimentModel 



