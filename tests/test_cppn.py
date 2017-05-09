
# ----- Update path for test -----

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

# ----- TEST -----

from evolearn.algorithms.neat import NEAT
import MultiNEAT as mneat
from viz import Draw
import numpy as np
import matplotlib.pyplot as plt

sim = NEAT(PopulationSize=300, verbose=True)
sim.run()

genome_list = mneat.GetGenomeList(sim.pop)


# Visualize the best network's genome
net = mneat.NeuralNetwork()

current_genome = sim.pop.Species[0].GetLeader()

sim.pop.Species[0].GetLeader().BuildPhenotype(net)
img = np.zeros((500, 500, 3), dtype=np.uint8)
img += 10
mneat.DrawPhenotype(img, (0, 0, 500, 500), net)

plt.imshow(img)
plt.show()



# # Pick out the genome
# current_genome = genome_list[0]

# Make a substrate meshgrid
resolution = 100
x = np.linspace(-1, 1, resolution)
y = np.linspace(-1, 1, resolution)
xv, yv = np.meshgrid(x, y)

response = []
for i in range(len(xv)):
    row = zip(xv[i], yv[i])
    row_out = []
    for loc in row:
        current_input = [ loc[0], loc[1], 1.0 ]
        fitness, output = sim.evaluate(current_genome, current_input)
        row_out.append(output[0])
    response.append(row_out)

plt.imshow(response)
plt.show()
