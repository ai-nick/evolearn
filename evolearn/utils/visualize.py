import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Animation:
    def __init__(self, data):
        """General purpose animation class using matplotlib.

        `Animation` creates an animation object from an arbitrary 3D array.

        # Example

        ```python
            sample = np.random.randn(100, 100, 60)
            anim = Animation(sample)
            anim.animate()
        ```

        # Input shape
            numpy array with shape: `(rows, cols, number_of_frames)`.

        # Output
            matplotlib Artist Animation object instance. 
            
        # TODO
            Update animation save protocols. Include save path definition option.


        """

        self.fig = plt.figure()
        self.frames = [[plt.imshow(data[:, :, frame], animated=True)] for frame in range(data.shape[2])]

        # Set up formatting for saving an animation
        # self.save_animation = True
        # Writer = animation.writers['ffmpeg']
        # self.writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    def animate(self):
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=50, blit=True, repeat_delay=1000)
        plt.axis('off')
        plt.show()
        # if self.save_animation:
        #     ani.save('im.mp4', writer=self.writer)

