
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
from PIL import Image

class DummyPics():

    """
    Generate dummy images with np.random.randn
    """

    def __init__(self, scale):

        self.num_images = 18

        if scale:
            self.image_scale = 16
            self.image_size = 8
        else:
            self.image_scale = 1
            self.image_size = 128

        self.raw = self.return_images()

    def return_images(self):

        return { img: self.generate_random_image() for img in range(self.num_images)}

    def generate_random_image(self):

        raw = np.random.randn(self.image_size, self.image_size)
        # raw = np.random.randint(10) * np.ones((self.image_size, self.image_size))
        slice = np.kron(raw, np.ones((self.image_scale, self.image_scale)))

        return_image = np.zeros((slice.shape[0], slice.shape[1], 3))

        for pane in range(3):
            return_image[:, :, pane] = slice

        return return_image

class PicGrid():

    def __init__(self, scale):

        # Make dummy image arrays
        dummy = DummyPics(scale)

        self.images = dummy.raw

        self.save_images()

    def save_images(self):

        for img in self.images.keys():

            name = 'child%d.jpg' % (img,)

            scipy.misc.imsave(name, self.images[img])


# pg = PicGrid()
#
# print pg.images[0].shape
# plt.imshow(pg.images[0][:, :, 0])
# plt.show()
#
# a = scipy.misc.imread('child0.jpg')
# print a.shape