
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
from PIL import Image
from copy import copy

class DummyPics():

    """
    Generate dummy images with np.random.randn
    """

    def __init__(self, scale):

        self.num_images = 20

        if scale:
            self.image_scale = 16
            self.image_size = 8
        else:
            self.image_scale = 1
            self.image_size = 128

        self.raw = self.return_images()

        self.border = self.return_borders()

    def return_images(self):

        return { img: self.generate_random_image() for img in range(self.num_images)}

    def generate_random_image(self):

        raw = np.random.randn(self.image_size, self.image_size)

        slice_image = np.kron(raw, np.ones((self.image_scale, self.image_scale)))

        return_image = np.zeros((slice_image.shape[0], slice_image.shape[1], 3))

        for pane in range(3):
            return_image[:, :, pane] = slice_image
            # return_border[:, :, pane] = slice_border

        return return_image

    def return_borders(self):

        return { img: self.generate_border(img) for img in self.raw.keys() }

    def generate_border(self, index):

        current_border = copy(self.raw[index])
        wall_width = 5
        wall_value = 5

        for pane in range(3):
            current_border[:, 0:wall_width, pane] = wall_value * np.ones((current_border.shape[0], wall_width))
            current_border[0:wall_width, :, pane] = wall_value * np.ones((wall_width, current_border.shape[1]))

            current_border[:, current_border.shape[1] - wall_width:, pane] = wall_value * np.ones((current_border.shape[0], wall_width))
            current_border[current_border.shape[0] - wall_width:, :, pane] = wall_value * np.ones((wall_width, current_border.shape[1]))

        return current_border

class PicGrid():

    def __init__(self, scale):

        # Make dummy image arrays
        dummy = DummyPics(scale)

        self.images = dummy.raw
        self.pressed = dummy.border

        self.save_images()

    def save_images(self):

        for img in self.images.keys():

            name = 'child%d.jpg' % (img,)
            name_pressed = 'child%dpress.jpg' % (img,)

            scipy.misc.imsave(name, self.images[img])
            scipy.misc.imsave(name_pressed, self.pressed[img])


class NavigStringBuild:

    def __init__(self):

        self.num_cols = 5
        self.num_children = 16

        self.return_string = self.init_string()

        self.build_buttons()

    def init_string(self):
            return_string = '''
<Page>:
    cols: 5
'''

            # Back button

            return_string += '''\n    Button\n        text: '< BACK'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[0]) '''

            # Something button
            return_string += '''\n    Button\n        text: 'CLEAR'\n        on_press: root.clear_selections() '''

            # Center label
            return_string += '''\n    Button\n        background_normal: 'kiwi.jpg' ''' # Place to put/show current parent seed

            # Something button
            return_string += '''\n    Button\n        text: 'Save Parents as Seeds'\n        on_press: app.save_parents(root.selected, root.limits) '''

            # Check evolve/advance button
            return_string += '''\n    Button\n        text: str(app.check_app_access(root.selected, root.limits))\n        on_press: app.wrap_up(root.selected, root.limits) '''

            return return_string

    def build_buttons(self):

        # Potential parent buttons

        for button in range(self.num_cols * 4):

            button_id = button
            addition = '''\n    Button\n        label: %d\n        background_normal: 'child%dpress.jpg' if self.label in root.selected else 'child%d.jpg'\n        on_press: root.return_id(self) ''' % (
            button_id, button_id, button_id)
            self.return_string += addition

class MenuStringBuild():

    def __init__(self):

        self.num_cols = 2
        self.return_string = self.build_buttons()

    def build_buttons(self):

        return_string = '''
<Menu>:
    cols: 3
    Button
        background_normal: 'child0.jpg'
        on_press: root.parent.parent.load_slide(root.parent.parent.slides[1])
    Label:
        id: keep_track2
        text: str(app.title)
    Button
        background_normal: 'child11.jpg'
        on_press: root.parent.parent.load_slide(root.parent.parent.slides[2])
    '''

        return_string += '''\n    Button\n        text: 'Start from Scratch'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[1]) '''
        return_string += '''\n    Button\n        text: 'EXIT'\n        on_press: app.stop() '''
        return_string += '''\n    Button\n        text: 'Start from Saved Parent Seed'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[2]) '''

        return return_string

class LoadParentsStringBuild:
    def __init__(self):
        self.num_cols = 5
        self.num_children = 16

        self.return_string = self.init_string()

        self.build_buttons()

    def init_string(self):
        return_string = '''
<Seeds>:
    cols: 5
    '''

        # Back button

        return_string += '''\n    Button\n        text: '< BACK TO MENU'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[0]) '''

        # Something button
        return_string += '''\n    Button\n        text: '< BACK'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[0]) '''

        # Center label
        return_string += '''\n    Button\n        text: 'ZOOM IN' \n        on_press: root.selection_view(root.selected) '''

        return_string += '''\n    Button\n        label: str(id(root)) \n        text: 'NEXT >' \n        on_press: print str(id(root)) ''' # root.parent.parent.load_slide(root.parent.parent.slides[self.label+2]) '''
        # return_string += '''\n    Button\n        text: 'NEXT >' '''

        # return_string += '''\n    Label\n        id: keep_track\n        text: 'PICBREEDER' '''
        return_string += '''\n    Button\n        text: str(root.check_selected())\n        on_press: app.wrap_up(root.selected, root.limits) '''


        # Check evolve/advance button
        # return_string += '''\n    Button\n        text: str(root.check_selected())\n        on_press: app.wrap_up(root.selected, root.limits) '''
        # return_string += '''\n    Button\n        text: 'NEXT >' '''


        return return_string

    def build_buttons(self):
        # Potential parent buttons

        for button in range(self.num_cols * 4):
            button_id = button
            # addition = '''\n    Button\n        label: %d\n        background_normal: 'child%dpress.jpg' if self.label in root.selected else 'child%d.jpg'\n        on_press: root.return_id(self) ''' % (
            #     button_id, button_id, button_id)
            addition = '''\n    Button\n        label: %d\n        background_normal: 'child%dpress.jpg' if self.label in root.selected else 'child%d.jpg'\n        on_press: root.select_seed(self.label) ''' % (
                button_id, button_id, button_id)
            self.return_string += addition

