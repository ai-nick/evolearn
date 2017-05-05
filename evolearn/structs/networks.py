
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import numpy as np


class CPPN:

    def __init__(self):

        self.num_inputs = 5
        self.num_outputs = 4

        self.cppn = self.initialize_cppn()

        self.adjacency = nx.to_numpy_matrix(self.cppn)

        # self.edge_genome = nx.read_edgelist(self.cppn.edge)

    def initialize_cppn(self):

        # Initialize
        cppn = nx.DiGraph()

        # Add the nodes
        cppn.add_nodes_from([ node for node in range(self.num_inputs + self.num_outputs) ])

        # Add the edges
        connections = list(itertools.product(range(self.num_inputs), range(self.num_inputs, self.num_inputs + self.num_outputs)))
        cppn.add_edges_from([ self.connection_init(connection[0], connection[1]) for connection in connections])

        return cppn

    def node_init(self, node):

        struct = {'type': [], 'activation': []}

        if node in range(self.num_inputs):
            type = 'input'
        elif node in range(self.num_inputs, self.num_inputs + self.num_outputs):
            type = 'output'
        else:
            type = 'hidden'

        act = 'linear'
        struct['type'], struct['activation'] = type, act

        return struct

    def connection_init(self, out_node, in_node):

        struct = (out_node, in_node, {'weight': 0, 'innovation': out_node})
        struct[2]['weight'] = np.random.randn()

        return struct

    def visualize(self):

        # Draw the graph cppn with labels using matplotlib
        nx.draw_circular(self.cppn, with_labels=True, node_color='b', font_color='w')
        plt.axis('off')
        plt.savefig("path.png")
        plt.show()


cppn = CPPN()

# print cppn.cppn.__dict__['edge']
print cppn.cppn.edges()
print cppn.cppn.edge
# cppn.visualize()
