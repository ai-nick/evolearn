
###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################

from evolearn.examples import Parameters


param_file_PKG = 'neat_simple.txt'
param_file_CWD = 'cwd_params.txt'
param_file_DSK = '/home/chad/Desktop/desktop_params.txt'

paramsPKG = Parameters(param_file_PKG)
print paramsPKG.values['discover']

paramsCWD = Parameters(param_file_CWD)
print paramsCWD.values['discover']

paramsDSK = Parameters(param_file_DSK)
print paramsDSK.values['discover']

