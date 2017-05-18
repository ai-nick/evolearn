

###################################
# ----- Update path for test -----#
###################################

import os
import sys

cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)

###################################

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.carousel import Carousel
from kivy.uix.actionbar import ActionBar


# Form the Seed ScrollView

layout_seeds = GridLayout(cols=5, spacing=20, size_hint_y=None)
layout_seeds.bind(minimum_height=layout_seeds.setter('height'))

for i in range(100):
    btn = Button(text=str(i), size_hint_y=None, height=128)
    layout_seeds.add_widget(btn)

choices = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
choices.add_widget(layout_seeds)

# # Define the Scratch Navigation Bar
# action_seeds = ActionBar()
# action_seeds.add_widget(choices)

# Form the Scratch ScrollView

layout_scratch = GridLayout(cols=5, spacing=20, size_hint_y=None)
layout_scratch.bind(minimum_height=layout_scratch.setter('height'))

for j in range(30):
    btn = Button(text=str(j), size_hint_y=None, height=128)
    layout_scratch.add_widget(btn)

choices_scratch = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
choices_scratch.add_widget(layout_scratch)

# Form the Menu

menu = GridLayout(cols=3, spacing=20, size_hint_y=None)
menu.bind(minimum_height=menu.setter('height'))

for b in range(9):
    btn = Button(txt=str(b), size_hint_y=None, height = 128)
    menu.add_widget(btn)

# Define the App root

root = Carousel()
root.add_widget(menu)
root.add_widget(choices)
# root.add_widget(action_seeds)
root.add_widget(choices_scratch)

# Run it

runTouchApp(root)