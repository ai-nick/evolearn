
###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################


# ----- TEST PARAMETER LOAD -----


from evolearn.examples.params import Parameters


params = Parameters('neat_simple.txt')


class Test:

    def __init__(self, parameters):

        self.neat_flavor = parameters['neat_flavor']
        self.environment_type = parameters['environment_type']
        self.population_size = parameters['population_size']
        self.max_evaluations = parameters['max_evaluations']
        self.num_generations = parameters['num_generations']
        self.num_repetitions = parameters['num_repetitions']
        self.verbose = parameters['verbose']
        self.performance_plotting = parameters['performance_plotting']
        self.visualize_leader = parameters['visualize_leader']


test = Test(params.values)
print test.__dict__
