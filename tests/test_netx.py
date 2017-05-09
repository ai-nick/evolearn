###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################


# ----- TEST -----

from evolearn.experiments.simulations import SimulationNEAT
from evolearn.utils.visualize import VisualizeNetwork

import MultiNEAT as mneat


# Instantiate a Simulation
sim = SimulationNEAT('NEAT', population_size=300, max_evaluations=1, num_generations=100, verbose=True)

# Run it
sim.run()




# # Build the population
# sim = NEAT(PopulationSize=300)
#
# # Run the experiment
# sim.run()




#
#
# Pull out the Best Performer (Leader) Genotype and build its Phenotype
net = mneat.NeuralNetwork()
sim.alg.pop.Species[0].GetLeader().BuildPhenotype(net)

# Network characteristics for visualization

#   - NODES
out_node = [ net.connections[connection].source_neuron_idx for connection in range(len(net.connections))]
in_node = [ net.connections[connection].target_neuron_idx for connection in range(len(net.connections))]

nodes = list(set(out_node + in_node))

types = [ net.neurons[node].type for node in range(len(net.neurons))]


#   - CONNECTIONS
weights = [ net.connections[connection].weight for connection in range(len(net.connections))]

edges = zip(out_node, in_node)


# Construct the Visualization
viz = VisualizeNetwork(nodes, edges, types, sim.num_inputs, sim.num_outputs)
viz.draw_networkx_NEAT()


