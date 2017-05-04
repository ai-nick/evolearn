
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animation:

    """A general purpose animation class using matplotlib.

    `Animation` creates an animation object from an arbitrary 3D array.

    :param data: 3D-array. For example, a single agent's decisions in an environment.
    :type data: np.array

    :Example:

    ```python
        from evolearn.utils.visualize import Animation
        import numpy as np
            
            
        world_size, num_frames = 300, 60
        data = np.random.randn(world_size, world_size, num_frames)
            
        anim = Animation(data)
        anim.animate()
    ```

    """

    def __init__(self, data):

        self.interval = 50
        self.blit = True
        self.repeat_delay = 1000

        self.fig = plt.figure()
        self.frames = [[plt.imshow(data[:, :, frame], animated=True)] for frame in range(data.shape[2])]

    def animate(self):

        """animate function for actually generating Animation figure from object instance.
        """

        ani = animation.ArtistAnimation(self.fig, self.frames, interval=self.interval, blit=self.blit, repeat_delay=self.repeat_delay)
        plt.axis('off')

        plt.show()


