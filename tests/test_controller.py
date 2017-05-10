###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################


# ----- TEST CONTROLLER -----

from evolearn.environments.environment_simple import SimpleEnvironment

env = SimpleEnvironment()

env.reset()
print env.agent.location