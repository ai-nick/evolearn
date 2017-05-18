
# ----- Update path for test -----

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

# ----- TEST -----

from evolearn.algorithms.neat import NEAT
import MultiNEAT as mneat

sim = NEAT(PopulationSize=10, verbose=True)

# pop.run()

# genome_list = mneat.GetGenomeList(sim.pop)
#
# current_genome = genome_list[0]
# # print current_genome
#
# net = mneat.NeuralNetwork()
# current_genome.BuildPhenotype(net)
#
# print dir(current_genome)
# print '\n', dir(net)
# print net.neurons
# print net.connections
