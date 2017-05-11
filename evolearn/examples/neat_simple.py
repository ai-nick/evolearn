###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(os.path.dirname(cwd))
sys.path.insert(0, project_root)

###################################


# ----- SIMPLE EXAMPLE SIMULATION -----

from evolearn.examples.params import Parameters
from evolearn.experiments.simulations import SimulationNEAT


# Pull example experiment parameters
params = Parameters('neat_simple.txt')

# Instantiate a Simulation
sim = SimulationNEAT(params.values)

# Run it
sim.run()




