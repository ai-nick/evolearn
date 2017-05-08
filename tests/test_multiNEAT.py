
# ----- Update path for test -----

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

# ----- TEST -----

from evolearn.population.population import NEAT

pop = NEAT()
pop.run()


