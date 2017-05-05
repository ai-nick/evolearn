
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

### NODES

num_inputs, num_outputs = 5, 1

cppn = nx.Graph()

# Add the nodes
cppn.add_nodes_from(range(num_inputs+num_outputs))

def connection_init( out_node, in_node ):
    struct = ( out_node, in_node, {'weight': 0})
    struct[2]['weight'] = np.random.randn()
    return struct

cppn.add_edges_from([connection_init(out_node, num_inputs) for out_node in range(num_inputs)])

a = cppn.__dict__

# print 'Number of nodes:', cppn.number_of_nodes()
# print 'Number of edges:', cppn.number_of_edges()
#
# for key in a.keys():
#     print '\n', key
#     print a[key]
#
# print cppn.nodes()
# print cppn.edges()
# print cppn.neighbors(3)


# Create a directed graph from the edges defined in cppn
cppn_final = nx.DiGraph(cppn)

a = cppn_final.__dict__

print 'Number of nodes:', cppn_final.number_of_nodes()
print 'Number of edges:', cppn_final.number_of_edges()

for key in a.keys():
    print '\n', key
    print a[key]

print cppn_final.nodes()
print cppn_final.edges()
print cppn_final.neighbors(3)

# Draw the graph G with matplotlib
# nx.draw(cppn_final)

# Draw the graph G using matplotlib
# nx.draw_networkx(cppn_final)

# Draw the nodes of the graph G
# nx.draw_networkx_nodes(cppn_final, pos=cppn_final.__dict__['node'] )

# Draw the graphG with spring layout
nx.draw_spring(cppn_final)


# nx.draw_circular(cppn_final)
plt.axis('off')
plt.show()
