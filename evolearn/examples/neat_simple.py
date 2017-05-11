
########################################################
#   ____  _      ___   _     ____   __    ___   _      #
#  | |_  \ \  / / / \ | |   | |_   / /\  | |_) | |\ |  #
#  |_|__  \_\/  \_\_/ |_|__ |_|__ /_/--\ |_| \ |_| \|  #
#                                                      #
#                  Chad Carlson - 2017                 #
########################################################


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
sim = SimulationNEAT(params)

# Run it
sim.run()




