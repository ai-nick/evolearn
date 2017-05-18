
import pkg_resources as pkg

__all__ = [ 'MenuBuilder' ]

class MenuBuilder:

    def __init__(self):

        self.num_cols = 3
        self.spacing = 10
        self.return_string = self.init_string()

        self.build()

    def init_string(self):

        return '''<Menu>:\n    cols: %d\n    spacing: %d''' % (self.num_cols, self.spacing)

    def build(self):

        # Visualize Start from Scratch CPPN
        # self.return_string += '''\n    Button\n        text: 'Scratch Example' '''
        self.return_string += '''\n    Label:\n        text: '' '''
        # self.return_string += '''\n    Button\n        background_normal: 'child0.jpg'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[1]) '''

        # Center Application Title
        self.return_string += '''\n    Label:\n        text: str(app.title) '''

        # Visualize Start from Seed Example CPPN
        self.return_string += '''\n    Label:\n        text: '' '''
        # self.return_string += '''\n    Button\n        background_normal: 'child0.jpg'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[1])'''

        # Start from Scratch Button
        # self.return_string += '''\n    Button\n        text: 'Start from Scratch' '''
        self.return_string += '''\n    Button\n        text: 'Start from Scratch'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[1]) '''

        # Center Exit Button
        self.return_string += '''\n    Label:\n        text: '' '''

        # Start from Seed Button
        self.return_string += '''\n    Button\n        text: 'Start from Saved Parent Seed' '''
        # self.return_string += '''\n    Button\n        text: 'Start from Saved Parent Seed'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[2]) '''

        self.return_string += '''\n    Label:\n        text: '' '''
        # self.return_string += '''\n    Button\n        background_normal: 'child0.jpg'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[1]) '''

        # Center Application Title
        self.return_string += '''\n    Button\n        text: 'EXIT'\n        on_press: app.stop() '''

        # Visualize Start from Seed Example CPPN
        self.return_string += '''\n    Label:\n        text: '' '''

class SelectMultipleBuilder:

    def __init__(self):

        self.num_cols = 5
        self.spacing = 10
        self.num_options = 20
        self.return_string = self.init_string()

        self.build_navigation_bar()

        self.build()

    def init_string(self):
        return '''\n<SelectMultiple>:\n    cols: %d\n    spacing: %d''' % (self.num_cols, self.spacing)

    def build_navigation_bar(self):

        # Back To Menu Button
        self.return_string += '''\n    Button\n        text: '< BACK'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[0]) '''

        # Clear selections Button
        self.return_string += '''\n    Button\n        text: 'CLEAR' '''
        # self.return_string += '''\n    Button\n        text: 'CLEAR'\n        on_press: root.clear_selections() '''

        # Current Parent Dummy Button
        self.return_string += '''\n    Button\n        text: 'Current Parent' '''
        # self.return_string += '''\n    Button\n        background_normal: 'kiwi.jpg' '''  # Place to put/show current parent seed

        # Save Selected Parents as Future Seeds Button
        self.return_string += '''\n    Button\n        text: 'Save as Seeds' '''
        # self.return_string += '''\n    Button\n        text: 'Save Parents as Seeds'\n        on_press: app.save_parents(root.selected, root.limits) '''

        # Dynamic Evolve/Advance Button
        self.return_string += '''\n    Button\n        text: 'EVOLVE >' '''
        # self.return_string += '''\n    Button\n        text: str(app.check_app_access(root.selected, root.limits))\n        on_press: app.wrap_up(root.selected, root.limits) '''

    def build(self):

        # Potential parent buttons

        for button in range(self.num_options):

            header = '''\n    Button'''
            label = '''\n        label: %d''' % (button, )
            img_press = '''\n        background_normal: app.pressed_define(self.label) if self.label in root.select_breed'''
            img_normal = ''' else app.normal_define(self.label)'''
            press_action = '''\n        on_press: root.return_id(self)'''

            self.return_string += header + label + img_press + img_normal + press_action

class SelectSingleBuilder:

    def __init__(self):

        self.num_cols = 5
        self.spacing = 10
        self.num_options = 20

        self.return_string = self.init_string()

        self.build_navigation_bar()

    def init_string(self):
        return '''\n<SelectSingle>:\n    cols: %d\n    spacing: %d''' % (self.num_cols, self.spacing)

    def build_navigation_bar(self):

        # Back To Menu Button
        self.return_string += '''\n    Button\n        text: '< BACK'\n        on_press: root.parent.parent.load_slide(root.parent.parent.slides[0]) '''

        # Clear selections Button
        self.return_string += '''\n    Button\n        text: 'CLEAR' '''
        # self.return_string += '''\n    Button\n        text: 'CLEAR'\n        on_press: root.clear_selections() '''

        # Current Parent Dummy Button
        self.return_string += '''\n    Button\n        text: 'Current Parent' '''
        # self.return_string += '''\n    Button\n        background_normal: 'kiwi.jpg' '''  # Place to put/show current parent seed

        # Save Selected Parents as Future Seeds Button
        self.return_string += '''\n    Button\n        text: 'Save as Seeds' '''
        # self.return_string += '''\n    Button\n        text: 'Save Parents as Seeds'\n        on_press: app.save_parents(root.selected, root.limits) '''

        # Dynamic Evolve/Advance Button
        self.return_string += '''\n    Button\n        text: 'EVOLVE >' '''
        # self.return_string += '''\n    Button\n        text: str(app.check_app_access(root.selected, root.limits))\n        on_press: app.wrap_up(root.selected, root.limits) '''
