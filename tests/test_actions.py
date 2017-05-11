
# ----- Update path for test -----

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

# ----- TEST -----

from evolearn.environments.environment_simple import SimpleEnvironment

env = SimpleEnvironment()

init_observation = env.reset()

print env.observation_space, len(init_observation)
print init_observation
