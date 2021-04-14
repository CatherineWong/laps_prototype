"""
model_base.py | Author : Catherine Wong

General purpose entrypoint for defining models.
"""

# Condition on constants.

class ModelBase():
    def init(model_config=None,
             experiment_state=None):
        # Initializes a model using its model-specific configuration block.
        # Passes in the experiment_state if it is necessary.
        # The initialization pattern is to define, for each of the possible functions, the parameters for 
        pass
    
    def checkpoint():
        # Writes out a model checkpoint to the checkpoint directory. 
        pass
    
    def update(condition_on=None,           experiment_state=None):
        # Updates the model parameters.
        # condition_on: a dictionary indicating 
        # what kinds of data we are conditioning on.
        # experiment_data: the experiment data object containing information that can be conditioned on..
        pass
    
    def generate(condition_on=None, experiment_data=None, **kwargs):
        # Generates from the model.
        # condition_type: a dictionary indicating 
        # what kinds of data we are conditioning on.
        pass
    
    
        