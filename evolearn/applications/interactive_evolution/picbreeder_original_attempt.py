
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

import glob

from .kv_builder import MenuBuilder, SelectMultipleBuilder, SelectSingleBuilder


__all__ = ['PicBreeder', 'Menu', 'SelectMultiple', 'SelectSingle']

menu = MenuBuilder()
select_from_scratch = SelectMultipleBuilder()
select_from_seed = SelectSingleBuilder()

Builder.load_string(menu.return_string + select_from_scratch.return_string + select_from_seed.return_string)

class PicBreeder(App):

    def build(self):

        self.images_normal, self.images_pressed = self.init_images()

        self.title = 'PicBreeder Interactive Evolution'

        self.selected_parents = ListProperty([])
        self.saved_parents = ListProperty([])

        root = Carousel()

        # Menu page
        root.add_widget(Menu())

        # Select (Single) from Seed Pages
        for page in range(3):
            root.add_widget(SelectSingle())

        # Select (Multiple) from Scratch Parent Page
        root.add_widget(SelectMultiple())

        return root

    def init_images(self):

        # These paths should be more general for the current users sys path. These folders will need to be generated each time app is run.
        normal_location = '/home/chad/Documents/research/evolearn/evolearn/applications/interactive_evolution/imgs/normal/*.jpg'
        image_normal_list = []

        for filename in glob.glob(normal_location):
            image_normal_list.append(filename)

        pressed_location = '/home/chad/Documents/research/evolearn/evolearn/applications/interactive_evolution/imgs/pressed/*.jpg'
        image_pressed_list = []

        for filename in glob.glob(pressed_location):
            image_pressed_list.append(filename)

        return image_normal_list, image_pressed_list

    def normal_define(self, id):
        return self.images_normal[id]

    def pressed_define(self, id):
        return self.images_pressed[id]

class Menu(GridLayout):
    pass

class SelectMultiple(GridLayout):

    select_breed = ListProperty([])
    select_breed_limits = [ 5, 8 ]

    select_seed = ListProperty([])
    select_seed_limits = [ 5, 8 ]

    def return_id(self, caller):

        self.check_parents(caller.label)

    def check_parents(self, selected):

        # Remove double-clicked parents
        if selected in self.select_breed:
            self.select_breed.remove(selected)

        # Add new parents
        else:
            self.select_breed.append(selected)

    def clear_selections(self):
        self.select_breed = []

class SelectSingle(GridLayout):

    select_parent = ListProperty([])