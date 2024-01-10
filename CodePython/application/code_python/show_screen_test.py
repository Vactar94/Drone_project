from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

from code_python.joystick.joystick import Joystick
from code_python.better_Kivy import Better_Screen

class Test_Screen(Better_Screen) :
    def __init__(self, **kw):
        super().__init__(**kw)

        box = FloatLayout()
        joy_r = Joystick(size_hint=(1.0/4.0, 1.0/4.0), pos_hint={"center_x":0.3,"center_y":0.7})
        joy_l = Joystick(size_hint=(1.0/4.0, 1.0/4.0), pos_hint={"center_x":0.3,"center_y":0.3})
        box.add_widget(joy_r)
        box.add_widget(joy_l)

        self.add_widget(box)

