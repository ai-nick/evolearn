
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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


