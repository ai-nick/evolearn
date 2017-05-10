###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################


# ----- TEST SIMULATION -----

from evolearn.experiments.simulations import SimulationNEAT


# Instantiate a Simulation
sim = SimulationNEAT('NEAT', population_size=250, max_evaluations=5, num_generations=50, verbose=True, visualizeLeader=True)

# Run it
sim.run()




