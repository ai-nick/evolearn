###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################

from evolearn.experiments import Experiment


# Define the experiment with a parameter file

exp = Experiment('cwd_params.txt')

# Run the experiment

exp.run()
