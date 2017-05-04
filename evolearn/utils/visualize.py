
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animation:

    def __init__(self, data):

        """General purpose animation class using matplotlib.

        `Animation` creates an animation object from an arbitrary 3D array.

        # Example

        ```python
            from evolearn.utils.visualize import Animation
            import numpy as np
            
            
            world_size, num_frames = 300, 60
            data = np.random.randn(world_size, world_size, num_frames)
            
            anim = Animation(data)
            anim.animate()
        ```

        # Input shape
            numpy array with shape: `(rows, cols, number_of_frames)`.

        # Output
            matplotlib Artist Animation object instance. 
            
        # TODO
            Update animation save protocols. Include save path definition option.

        """

        self.interval = 50
        self.blit = True
        self.repeat_delay = 1000

        self.fig = plt.figure()
        self.frames = [[plt.imshow(data[:, :, frame], animated=True)] for frame in range(data.shape[2])]

        # Set up formatting for saving an animation
        # self.save_animation = True
        # Writer = animation.writers['ffmpeg']
        # self.writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    def animate(self):
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=self.interval, blit=self.blit, repeat_delay=self.repeat_delay)
        plt.axis('off')
        plt.show()

        # if self.save_animation:
        #     ani.save('im.mp4', writer=self.writer)

