from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

Builder.load_string("""
<MyScreenManager>
    Screen:
        name: 'questionary'
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Question 1'
                on_press: root.question = self; root.current = 'question_1'
                background_normal: 'kiwi.jpg'
            Button:
                text: 'Question 2'
                on_press: root.question = self; root.current = 'question_1'
                background_normal: 'kiwi.jpg'
    Screen:
        name: 'question_1'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Are you going to answer this question?'
            Button:
                text: 'Yes'
                on_press: root.question.background_normal = 'child0.jpg'; root.current = 'questionary'
""")


class MyScreenManager(ScreenManager):
    pass

class TestApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    TestApp().run()