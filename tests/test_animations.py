
import os
import sys

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, project_root)

from evolearn.utils.visualize import Animation
import numpy as np


world_size, num_frames = 300, 60
data = np.random.randn(world_size, world_size, num_frames)

anim = Animation(data)
anim.animate()
