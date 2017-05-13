from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.lang import Builder

from button_grid import PicGrid


#
# Builder.load_string('''
# <Button>:
#     Button
#         label: 0
#         background_normal: 'child0.jpg'
# ''')
        
class TestApp(App):

    selected_parents = ListProperty([])

    def build(self):

        def on_press():
            print 9

        self.title = 'PicBreeder Demo'

        root = GridLayout(cols=5)  # TODO - Dynamic columns
        root.add_widget(Button(text='Generation X'))  # TODO - Dynamic Generation updates

        for parent in range(18):

            image = 'child' + str(parent) + '.jpg'
            root.add_widget(Button(label=parent, background_normal=image) )
            # root.add_widget(Button(label=parent, background_normal=image, on_press=on_press()))
            # TODO - on_press: push selected id to global list (selection)
            # TODO - selected: alternative border select img (bounding box?)

        root.add_widget(Button(text='Evolve (min, max = 3, 8)')) # TODO - enforce min, max

        return root



if __name__ == '__main__':

    # Build the Images from the arrays

    scale = True
    pg = PicGrid(scale)

    # Build the app

    a = TestApp()

    # Run the app

    a.run()
