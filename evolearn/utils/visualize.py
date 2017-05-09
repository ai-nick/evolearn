
####################################
# ----------- evolearn ----------- #
####################################


import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

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


class VisualizeNetwork:

    def __init__(self, nodes, edges, types, num_inputs, num_outputs):

        self.nodes = nodes
        self.edges = edges
        self.types = types
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.scale = 5

    def draw_networkx_NEAT(self):

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

        nx.draw_networkx(net, pos=locations, node_color='b', font_color='w')
        plt.axis('off')
        plt.show()


