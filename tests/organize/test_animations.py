
# ----- Update path for test -----

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

# ----- TEST -----

from evolearn.utils.visualize import Animation
import numpy as np


world_size, num_frames = 300, 60
data = np.random.randn(world_size, world_size, num_frames)

anim = Animation(data)
anim.animate()
