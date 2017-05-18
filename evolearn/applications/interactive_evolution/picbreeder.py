
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button


import glob

from kv_builder import MenuBuilder, SelectMultipleBuilder, SelectSingleBuilder

__all__ = ['PicBreeder']


menu = MenuBuilder()
select_from_scratch = SelectMultipleBuilder()
select_from_seed = SelectSingleBuilder()

Builder.load_string(menu.return_string + select_from_scratch.return_string + select_from_seed.return_string)

class PicBreeder(App):

    location_saved_seeds = '/home/chad/Documents/research/evolearn/evolearn/applications/interactive_evolution/saved_seeds/'
    location_scratch_seeds = '/home/chad/Documents/research/evolearn/evolearn/applications/interactive_evolution/scratch_seeds/'

    normal_images = 'imgs/normal/'
    pressed_images = 'imgs/pressed/'

    title = 'PicBreeder'
    num_columns = 4
    spacing = 10

    selected_from_scratch = ListProperty([])
    selected_from_seeds = ListProperty([])
    saved_parents = ListProperty([])

    def build(self):

        self.images_normal, self.images_pressed = self.init_images()

        # Start (multiple) from Scratch Page
        scratch_layout = SelectMultiple()
        scratch_layout.bind(minimum_height=scratch_layout.setter('height'))
        scratch_scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scratch_scroll.add_widget(scratch_layout)

        # Select (Single) from Seed Pages
        seed_grid = GridLayout(cols=self.num_columns, spacing=self.spacing, size_hint_y=None)
        seed_grid.bind(minimum_height=seed_grid.setter('height'))

        for j in range(30):

            if j > self.num_columns - 1:

                btn = Button(label=j, size_hint_y=None, height=128)

                btn.background_normal = self.load_saved_parent_image(btn.label)

            else:

                btn = Button(text='MENU', size_hint_y=None, height=50)

            # btn.on_press = self.add_saved_parent_to_selected(btn.label)

            seed_grid.add_widget(btn)

        seed_scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        seed_scroll.add_widget(seed_grid)

        # Define the root application
        root = Carousel()
        root.add_widget(Menu())
        root.add_widget(scratch_scroll)
        root.add_widget(seed_scroll)

        return root

    def add_saved_parent_to_selected(self, id):

        # print self.selected_from_seeds

        if self.selected_from_seeds:

            if id in self.selected_from_seeds:
                self.selected_from_seeds.remove(id)
            else:
                self.selected_from_seeds.append(id)


    def load_saved_parent_image(self, id):

        image_string_normal = self.location_saved_seeds + self.normal_images + 'parent' + str(id - id) + '.jpg'
        image_string_pressed = self.location_saved_seeds + self.pressed_images + 'parent' + str(id - id) + 'press.jpg'
        image_string = '''''' + image_string_pressed + ''' if ''' + str(id) + ''' in self.selected_from_seeds else ''' + image_string_normal + ''''''

        return image_string

    def init_images(self):

        # These paths should be more general for the current users sys path. These folders will need to be generated each time app is run.
        normal_location = self.location_scratch_seeds + self.normal_images  + '*.jpg'
        image_normal_list = []

        for filename in glob.glob(normal_location):
            image_normal_list.append(filename)

        pressed_location = self.location_scratch_seeds + self.pressed_images + '*.jpg'
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


pb = PicBreeder()
pb.run()
