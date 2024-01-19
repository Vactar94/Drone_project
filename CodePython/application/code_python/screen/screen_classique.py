from code_python.screen.screen_stremable import Screen_Stramable
from code_python.joystick import Joystick

from kivy.uix.floatlayout import FloatLayout

class Screen_Classique(Screen_Stramable) :
    def __init__(self,**kwargs):

        super().__init__(**kwargs)
        box_contol = FloatLayout()
        joy_r = Joystick(size_hint=(1.0/2.5, 1.0/2.5), pos_hint={"center_x":0.3,"center_y":0.7})
        joy_l = Joystick(size_hint=(1.0/2.5, 1.0/2.5), pos_hint={"center_x":0.3,"center_y":0.3})
        box_contol.add_widget(joy_r)
        box_contol.add_widget(joy_l)
        
        self.add_widget(box_contol)