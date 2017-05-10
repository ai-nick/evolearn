
####################################
# ----------- evolearn ----------- #
####################################


import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import MultiNEAT as mneat
import networkx as nx


class Animation:

    """A general purpose animation class using matplotlib.

    `Animation` creates an animation object from an arbitrary 3D array.

    :param data: 3D-array. For example, a single agent's decisions in an environment.
    :type data: np.array

    """

    def __init__(self, data):

        self.interval = 50
        self.blit = True
        self.repeat_delay = 1000

        self.fig = plt.figure()
        self.frames = [[plt.imshow(data[:, :, frame], animated=True)] for frame in range(data.shape[2])]

    def animate(self):

        """animate function for actually generating figure from Animation instance.
        """

        ani = animation.ArtistAnimation(self.fig, self.frames, interval=self.interval, blit=self.blit, repeat_delay=self.repeat_delay)
        plt.axis('off')

        plt.show()


class VisualizeLeader:

    def __init__(self, sim, num_inputs, num_outputs, NEAT_flavor):

        self.sim = sim
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.NEAT_flavor = NEAT_flavor

        self.scale = 5

        self.draw_networkx_NEAT()

    def reformat_sim_info(self):

        # Pull out the Best Performer (Leader) Genotype and build its Phenotype
        net = mneat.NeuralNetwork()
        self.sim.pop.Species[0].GetLeader().BuildPhenotype(net)

        # Network characteristics for visualization

        #   - NODES
        out_node = [net.connections[connection].source_neuron_idx for connection in range(len(net.connections))]
        in_node = [net.connections[connection].target_neuron_idx for connection in range(len(net.connections))]

        nodes = list(set(out_node + in_node))

        types = [net.neurons[node].type for node in range(len(net.neurons))]

        #   - CONNECTIONS
        weights = [net.connections[connection].weight for connection in range(len(net.connections))]

        edges = zip(out_node, in_node)

        return nodes, types, edges, weights

    def draw_networkx_NEAT(self):

        # Pull node and connection information from the completed simulation
        self.nodes, self.types, self.edges, self.weights = self.reformat_sim_info()

        index = {'input': 0, 'output': 0, 'hidden': 0}
        node_types = {'input': [0, 1, 2], 'output': [4], 'hidden': [3]}

        # Define the network
        net = nx.DiGraph()

        # Add the nodes
        net.add_nodes_from(self.nodes)

        # Define node locations
        input_locations = [(x, -self.scale * 1.0) for x in np.linspace(self.scale * -1, self.scale * 1, self.num_inputs)]
        if self.num_outputs == 1:
            output_locations = [(0.0, self.scale * 1.0)]
        else:
            output_locations = [(x, self.scale * 1.0) for x in np.linspace(self.scale * -1, self.scale * 1, self.num_outputs)]

        locations = dict.fromkeys(self.nodes)
        for node in self.nodes:
            if self.types[node] in node_types['input']:
                locations[node] = input_locations[index['input']]
                index['input'] += 1
            elif self.types[node] in node_types['output']:
                locations[node] = output_locations[index['output']]
                index['output'] += 1
            elif self.types[node] in node_types['hidden']:
                locations[node] = (self.scale * np.random.uniform(-0.9, 0.9), self.scale * np.random.uniform(-0.9, 0.9))
                index['hidden'] += 1

        # Add the connections
        net.add_edges_from(self.edges)

        if self.NEAT_flavor != 'NEAT':
            plt.subplot(1,2,1)
            plt.title(self.NEAT_flavor + ' Genotype')
            nx.draw(net, pos=locations, node_color='b', font_color='w')
            plt.axis('off')

            plt.subplot(1,2,2)
            plt.title(self.NEAT_flavor + ' Phenotype')
            nx.draw(net, pos=locations, node_color='r', font_color='w')
            plt.axis('off')

        else:
            plt.title(self.NEAT_flavor + ' Phenotype')
            nx.draw(net, pos=locations, node_color='r', font_color='w')
            plt.axis('off')


        plt.show()


