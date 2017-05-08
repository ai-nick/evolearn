
# ----- Update path for test -----

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

# ----- TEST -----

from old_ditch import CPPN

agent1 = CPPN()
agent2 = CPPN()

print agent1.cppn.node
print agent2.cppn.node
# print agent1.cppn.edge

# print agent1.adjacency