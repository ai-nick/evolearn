'''
Carousel example with button inside.
This is a tiny test for testing the scroll distance/timeout
And ensure the down/up are dispatched if no gesture is done.
'''
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, ObservableList, ObjectProperty

from button_grid import PicGrid

# Make this Builder more systematic with an object (or from within PicGrid)

Builder.load_string('''
<Page>:
    cols: 5
    Label:
        id: keep_track
        text: str(root.selected)
    Button
        label: 0
        background_normal: 'child0.jpg'
        background_down: 'kiwi.jpg'
        border: (2, 2, 2, 2)
        on_press: root.return_id(self)
    Button
        label: 1
        background_normal: 'child1.jpg'
        on_press: root.return_id(self)
    Button
        label: 2
        background_normal: 'child2.jpg'
        on_press: root.return_id(self)
    Button
        label: 3
        background_normal: 'child3.jpg'
        on_press: root.return_id(self)
    Button
        label: 4
        background_normal: 'child4.jpg'
        on_press: root.return_id(self)
    Button
        label: 5
        background_normal: 'child5.jpg'
        on_press: root.return_id(self)
    Button
        label: 6
        background_normal: 'child6.jpg'
        on_press: root.return_id(self)
    Button
        label: 7
        background_normal: 'child7.jpg'
        on_press: root.return_id(self)
    Button
        label: 8
        background_normal: 'child8.jpg'
        on_press: root.return_id(self)
    Button
        label: 9
        background_normal: 'child9.jpg'
        on_press: root.return_id(self)
    Button
        label: 10
        background_normal: 'child10.jpg'
        on_press: root.return_id(self)
    Button
        label: 11
        background_normal: 'child11.jpg'
        on_press: root.return_id(self)
    Button
        label: 12
        background_normal: 'child12.jpg'
        on_press: root.return_id(self)
    Button
        label: 13
        background_normal: 'child13.jpg'
        on_press: root.return_id(self)
    Button
        label: 14
        background_normal: 'child14.jpg'
        on_press: root.return_id(self)
    Button
        label: 15
        background_normal: 'child15.jpg'
        on_press: root.return_id(self)
    Button
        label: 16
        background_normal: 'child16.jpg'
        on_press: root.return_id(self)
    Button
        label: 17
        background_normal: 'child17.jpg'
        on_press: root.return_id(self)
    Button
        text: str(app.check_app_access(root.selected, root.limits))
        on_press: app.wrap_up(root.selected, root.limits)
''')


class Page(GridLayout):

    selected = ListProperty([])
    limits = [ 3, 8 ] # [ min parents, max parents ]

    def return_id(self, caller):

        self.check_parents(caller.label)

    def check_parents(self, selected):

        # Remove double-clicked parents
        if selected in self.selected:
            self.selected.remove(selected)

        # Add new parents
        else:
            self.selected.append(selected)

        # Enforce maximum parents
        if len(self.selected) > self.limits[1]:
            self.selected.pop(0)



class TestApp(App):

    selected = ListProperty([])

    def build(self):

        root = Carousel()
        p = Page()
        root.add_widget(p)
        self.selected = root.ids
        return root

    def wrap_up(self, selected, limits):

        if len(selected) >= limits[0] and len(selected) <= limits[1]:

            self.selected = selected
            self.stop()

    def check_app_access(self, selected, limits):
        if len(selected) < limits[0]:
            output = 'Add parents (min %d)' % (limits[0],)
        elif len(selected) > limits[1]:
            output = 'Remove parents (max %d)' % (limits[1], )
        else:
            output = 'EVOLVE!'
        return output



if __name__ == '__main__':

    # Construct the images
    scale = True
    pg = PicGrid(scale)

    # Build and run the app
    exp = TestApp()
    exp.run()

    # Retrieve the selected parent CPPNs
    print exp.selected
