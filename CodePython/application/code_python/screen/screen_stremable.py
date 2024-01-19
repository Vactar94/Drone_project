from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.image import Image

from code_python.tello import DRONE
from code_python.notification import NOTIF_MANAGER
from code_python.better_Kivy import Better_Screen
from code_python.global_function import is_wifi_drones_connected

class Screen_Stramable(Better_Screen) :
    
    def __init__(self, notifications: dict = None, **kw):
        super().__init__(notifications, **kw)
        self.streamable = True

        self.size = Window.size

        self.image_streem = Image(size=self.size)
        self.box_streem = BoxLayout(size_hint=(None,None), size=self.size)

        menue_button = Button(text="", color=(0 ,0 ,0), size_hint=(None,None), size=(60,60), pos_hint={"center_x":1-0.87,"center_y":0.9}, background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png",size=menue_button.size,pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue,size=self.update_bg,pos=self.update_bg)
        

        self.box_streem.add_widget(self.image_streem)
        self.add_widget(self.box_streem)
        self.add_widget(menue_button)


    def on_pre_enter(self) :
        """check que le drone est connecté, oui-> le streem commence puis notif l'app que le drone est co
                                            non -> notif l'app que le drone n'est pas co
        """        
        if is_wifi_drones_connected() and not DRONE.is_connected :
            DRONE.connect()
        a = DRONE.start_streeming()
        print(f"le streem a commencé : {a}")
        if not a :
            self.go_to_menue("ui")
            NOTIF_MANAGER.Waiting_notifications["D"][0] = True
        else : NOTIF_MANAGER.Waiting_notifications["D"][1] = True

    def on_pre_leave(self, *args):

        if DRONE.is_connected:
            DRONE.stop_streeming()
        return super().on_pre_leave(*args)
    

    def go_to_menue(self,value) :
        self.manager.current = "ui"