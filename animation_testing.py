

from evolearn.utils.visualize import Animation
import numpy as np


world_size, num_frames = 300, 60
data = np.random.randn(world_size, world_size, num_frames)

anim = Animation(data)
anim.animate()

