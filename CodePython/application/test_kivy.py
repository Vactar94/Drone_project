from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout


class test_app (App) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) :
        sm = ScreenManager()
        test_screen = Test_Screen(name="test")
        sm.add_widget(test_screen)
        sm.current = "test"

        return sm



class Test_Screen (Screen) :
    def __init__(self, **kw):
        super().__init__(**kw)
        b = Button()
        b.bind(on_release=self.menu_button)

        image_button = Image(source="image/bouton-retour bg.png", size_hint=(0.3, 0.3),pos_hint={'center_x': 0.5, 'center_y': 0.5} )
        image_button = Image(source="image/bouton-retour bg_blanc.png", size_hint=(0.3, 0.3),pos_hint={'center_x': 0.5, 'center_y': 0.5} )
        self.add_widget(b)
        self.add_widget(image_button)
        

    def menu_button(self, button) :
        print("cliqué")

t = test_app()
t.run()