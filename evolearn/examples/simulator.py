
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

from evolearn.examples.params import Parameters
from evolearn.experiments.simulations import SimulationNEAT


# ----- TEMPLATE EXPERIMENT -----

class Experiment:

    def __init__(self, parameter_file):

        # Pull example experiment parameters

        self.params = Parameters(parameter_file)

        # Instantiate a Simulation

        if self.params.values['experiment_type'] == 'NEAT':

            # NEAT SIMULATION

            self.sim = SimulationNEAT(self.params)

    def run(self):

        self.sim.run()
