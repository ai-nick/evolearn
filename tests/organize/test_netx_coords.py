
import networkx as nx
import numpy as np
import itertools
import matplotlib.pyplot as plt


def draw_networkx_NEAT(nodes, edges, types, num_inputs, num_outputs):

    scale = 5

    index = { 'input': 0, 'output': 0, 'hidden': 0 }
    node_types = { 'input': [0, 1, 2], 'output': [4], 'hidden': [3] }

    # Define the network
    net = nx.DiGraph()

    # Add the nodes
    net.add_nodes_from(nodes)

    # Define node locations
    input_locations = [ (x, -scale*1.0) for x in np.linspace(scale*-1, scale*1, num_inputs)]
    if num_outputs == 1:
        output_locations = [(0.0, scale*1.0)]
    else:
        output_locations = [(x, scale*1.0) for x in np.linspace(scale*-1, scale*1, num_outputs)]

    locations = dict.fromkeys(nodes)
    for node in nodes:
        if types[node] in node_types['input']:
            locations[node] = input_locations[index['input']]
            index['input'] += 1
        elif types[node] in node_types['output']:
            locations[node] = output_locations[index['output']]
            index['output'] += 1
        elif types[node] in node_types['hidden']:
            locations[node] = ( scale*np.random.uniform(-0.9, 0.9 ), scale*np.random.uniform(-0.9, 0.9))
            index['hidden'] += 1

    # print nodes
    # print types
    # print locations

    # Add the connections
    net.add_edges_from(edges)

    nx.draw_networkx(net, pos=locations, node_color='b', font_color='w')
    plt.axis('off')
    plt.show()


# # Create the graph
# net = nx.DiGraph()
#
# num_inputs, num_outputs = 5, 1
#
# # Add the nodes
# num_neurons = num_inputs + num_outputs
# net.add_nodes_from(range(num_inputs+num_outputs))
# type = [ 1 for node in range(num_inputs-1) ] + [ 2 ] + [ 3 for node in range(num_outputs)]
#
# # Define node positions
# input_locations = [ (x, -1.0) for x in np.linspace(-1, 1, num_inputs)]
#
# if num_outputs == 1:
#     output_locations = [(0.0, 1.0)]
# else:
#     output_locations = [ (x, 1.0) for x in np.linspace(-1, 1, num_outputs)]
#
# all_locations = input_locations + output_locations
# locations = dict(zip(range(num_neurons), all_locations))
#
# # Add the connections
# edges = list(itertools.product(range(num_inputs), range(num_inputs, num_inputs+num_outputs)))
# net.add_edges_from(edges)
#
# # nx.draw_networkx(net, pos=locations, node_color='b', font_color='w')
# # plt.axis('off')
# # plt.show()
