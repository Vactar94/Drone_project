from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from code_python.better_Kivy import Better_Button, Better_Label



class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        upside_down_label = Better_Button(text="Hello, upside down!")
        layout.add_widget(upside_down_label)

        return layout

if __name__ == '__main__':
    MyApp().run()
