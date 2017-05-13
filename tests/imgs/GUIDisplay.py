from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import *

class RootWidget(FloatLayout):

    def add_transition_toggle(self):
        print 'something happened'

    def change_tape(self):
        pass

    def backgroundpress(self):
        print 'region'

    def actionbuttonpress(self):
        print 'menu'

    def on_touch_down(self, touch):
        event_handled = False
        for child in self.children:
            if not event_handled:
                if child.dispatch('on_touch_down', touch):
                    event_handled = True

        if not event_handled:
            print touch.x, touch.y

class GUIDisplay(App):

    def build(self):
        app = RootWidget()
        return app


def start_app():
    GUIDisplay().run()

if '__main__' == __name__:
    start_app()