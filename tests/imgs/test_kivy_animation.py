'''
Interactive Evolution for PicBreeder
'''


from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button


from button_grid import NavigStringBuild, MenuStringBuild, LoadParentsStringBuild
from button_grid import PicGrid


# Make this Builder more systematic with an object (or from within PicGrid)

sb = NavigStringBuild()
menu = MenuStringBuild()
parents_saved = LoadParentsStringBuild()


Builder.load_string(menu.return_string + sb.return_string + parents_saved.return_string)

class Page(GridLayout):

    selected = ListProperty([])
    save_parents_as_seeds = ListProperty([])

    limits = [ 5, 10 ] # [ min parents, max parents ]

    def return_id(self, caller):

        self.check_parents(caller.label)

    def check_parents(self, selected):

        # Remove double-clicked parents
        if selected in self.selected:
            self.selected.remove(selected)

        # Add new parents
        else:
            self.selected.append(selected)

    def clear_selections(self):
        self.selected = []

class Menu(GridLayout):

    pass

class Seeds(GridLayout):

    selected = ListProperty([])
    limits = [ 5, 10 ] # [ min parents, max parents ]

    def selection_view(self, id):

        if len(self.selected):

            id = id[0]

            image = 'child%d.jpg' % (id, )

            content = Button(background_normal=image)#, on_press=self.select_seed(id))

            popup = Popup(title='View Parent Seed', content=content, size_hint=(None, None), size=(500, 500), auto_dismiss=False)
            content.bind(on_press=popup.dismiss)

            popup.open()

    def select_seed(self, id):
        if not len(self.selected):
            self.selected.append(id)
        elif id in self.selected:
            self.selected.remove(id)
        else:
            self.selected[0] = id
        print self.selected

    def check_selected(self):

        if not len(self.selected):
            output = 'Choose Seed'
        else:
            output = 'EVOLVE SEED >'
        return output

    def clear_selections(self):
        self.selected = []

    def selected_icon(self):
        if self.selected:
            output = 'child%d.jpg' % (self.selected[0],)
        else:
            output = 'kiwi.jpg'
        return output



class TestApp(App):

    selected = ListProperty([])
    saved_parents = ListProperty([])

    def build(self):
        self.title = 'PicBreeder Interactive Evolution'
        root = Carousel()

        # Menu page
        root.add_widget(Menu()) # 0

        # Start from scratch page - One way to keep scratch and seeds separate would be to
        #   have one as odd indices and the other as the even (just remember the menu is = slide[0])

        # OR, alternatively, should the best solution be to launch a separate app for each, with its own numbering?

        # ALTHOUGH, if it is truly functional, the only difference between a SCRATCH and SEED trajectory should be the definition of those images.
        #   Therfore, it could instead be numbered [0]-menu, [1-x]: saved seeds, [x+1:]: interactive evolution based on selected seed (SCRATCH or SAVED)

        root.add_widget(Page()) # 1

        for seeds in range(3):

            # Start from saved seed page
            root.add_widget(Seeds()) # 2, 3, 4

        return root

    def wrap_up(self, selected, limits):

        if len(selected) >= limits[0] and len(selected) <= limits[1]:

            self.selected = selected
            self.stop()

    def check_app_access(self, selected, limits):
        if len(selected) < limits[0]:
            output = 'Add parents (min %d)' % (limits[0],)
        elif len(selected) > limits[1]:
            output = 'Too many (max %d)' % (limits[1], )
        else:
            output = 'EVOLVE >'
        return output

    def save_parents(self, selected, limits):

        if len(selected) >= limits[0] and len(selected) <= limits[1]:

            self.saved_parents = selected



if __name__ == '__main__':

    # Construct the images
    scale = True
    pg = PicGrid(scale)

    # Build and run the app
    exp = TestApp()
    exp.run()

    # Retrieve the selected parent CPPNs
    print exp.selected
    print exp.saved_parents
