from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color

from code_python.tello import DRONE
from code_python.langues.langues import UPDATE_MANAGER, Update_Button
from code_python.joystick.joystick import Joystick
from code_python.better_Kivy import Better_Screen

class Test_Screen(Better_Screen) :
    def __init__(self, **kw):
        super().__init__(**kw)

        # --------------------- control_box --------------------- #

        control_box = FloatLayout(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # --- joystiks --- #
        joy_r = Joystick(size_hint=(1.0/2.5, 1.0/2.5), pos_hint={"center_x":0.25,"center_y":0.8},
                         inner_background_color=(100/255, 50/255, 50/255, 0.2), 
                         pad_background_color=(220/255, 120/255, 120/255, 0.6), 
                         outer_background_color=(150/255, 40/255, 40/255, 0.1))
        joy_l = Joystick(size_hint=(1.0/2.5, 1.0/2.5), pos_hint={"center_x":0.25,"center_y":0.2}, 
                         inner_background_color=(50/255, 50/255, 100/255, 0.2), 
                         pad_background_color=(120/255, 120/255, 220/255, 0.6), 
                         outer_background_color=(40/255, 40/255, 150/255, 0.1))
        
        # --- land button --- #
        
        def land_button_text()->str :
            if DRONE.is_flying :
                return "app.drone.control.land_button.air"
            else :
                return "app.drone.control.land_button.sol"
            
        self.land_button = Update_Button(id_text="app.drone.control.land_button.sol",fncton=land_button_text,frequence=UPDATE_MANAGER.UPDATE_ALL_FRAME,
                                    pos_hint={"center_x":0.7,"center_y":0.15}, background_color=(1, 0, 1, 0.5), size_hint=(0.2,0.1), angle=-90)

        

        control_box.add_widget(self.land_button)
        control_box.add_widget(joy_r)
        control_box.add_widget(joy_l)
        
        # --------------------- return button --------------------- #
        menue_button = Button(text="", color=(0 ,0 ,0, 0), size_hint=(None,None), size=(60,60), pos_hint={"center_x":0.88,"center_y":0.915}, background_color=(0, 0, 0, 0))
        menue_button.bind(size=self.update_bg,pos=self.update_bg)
        with menue_button.canvas.before :
            Color(0, 0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg_blanc.png",size=menue_button.size, pos=menue_button.pos)
            menue_button.bg_rect
        menue_button.bind(on_release=self.go_to_menu)


        self.add_widget(control_box)
        self.add_widget(menue_button)





    def on_pre_enter(self, *args):
        self.land_button.update_rotation_origin(0, 0)
        return super().on_pre_enter(*args)
    
    def on_enter(self, *args):
        self.land_button.update_rotation_origin(0, 0)
        return super().on_enter(*args)

    def go_to_menu(self, button) :
        self.manager.current = "ui"

        