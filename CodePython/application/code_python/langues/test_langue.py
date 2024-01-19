from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from ..better_Kivy import Better_Button



class test_app(App) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.var = "Cliquez-moi"
        
    def build(self) :

        app_box = BoxLayout()

        button = Better_Button(text="bonjour")

        app_box.add_widget(button)

        
        return app_box
        



if __name__ == "__main__" :
    test_app().run()