from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager,RiseInTransition
from kivy.config import Config
from kivy.clock import Clock

from code_python.notification import crea_notif
from code_python.joystick.joystick import Joystick
from code_python.better_Kivy import Better_Screen, Screen_sous_menu, Screen_Stramable
from code_python.menue import Menue
from code_python.accueil import Accueil
from code_python.global_function import SYSTEM, is_wifi_drones_connected
from code_python.tello import DRONE
from code_python.notification import NOTIF_MANAGER
from code_python.screen_parametre import Screen_Parametre
from code_python.langues.langues import UPDATE_MANAGER
from code_python.screen_info_drone import Screen_Info_Drone
from code_python.show_screen_test import Test_Screen


Window.size = [360, 620]
#Window.size = [1000, 620]
Window.OS = SYSTEM


class The_app(App):
    """
    la main_app a partir du quel l'app se lance
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=RiseInTransition())
        self.dm = DRONE
        self.seconde = 0



    def build(self):
        #création des screens  
        notifs = crea_notif()
        ui_screen = UiScreen(name='ui', notifications=notifs.copy())
        controle_screen = Screen_Controles(name='controles', notifications=notifs.copy())
        parametre_screen = Screen_Parametre(name="parametre", notifications=notifs.copy())
        classique_screen = Screen_Classique(name="classique", notifications=notifs.copy())
        automatique_screen = Screen_Automatique(name="automatique", notifications=notifs.copy())
        screen_affiche = Screen_proj(name="affiche", notifications=notifs.copy())
        screen_info_drone = Screen_Info_Drone(name="info_drone", notifications=notifs.copy())
        test_screen = Test_Screen(name="test")

        # ajout des screens au screen manager

        self.sm.add_widget(ui_screen)
        self.sm.add_widget(classique_screen)
        self.sm.add_widget(screen_affiche)
        self.sm.add_widget(controle_screen)
        self.sm.add_widget(automatique_screen)
        self.sm.add_widget(parametre_screen)
        self.sm.add_widget(screen_info_drone)
        self.sm.add_widget(test_screen)

        Clock.schedule_interval(self.update_60_fps, 1.0 / 60.0)
        Clock.schedule_interval(self.update_30_fps, 1.0 / 30.0)
        Clock.schedule_interval(self.update_1_seconde, 1.0 / 1.0)
        Clock.schedule_interval(self.update_5_seconde, 5.0)
        Clock.schedule_interval(self.update_30_seconde, 30.0)
        
        return self.sm

    def update_30_seconde(self, dt) :
        self.seconde += 1
        UPDATE_MANAGER.update_all_30()

    def update_5_seconde(self, dt) :
        self.seconde += 1
        UPDATE_MANAGER.update_all_5()

    def update_1_seconde(self, dt) :
        self.seconde += 1
        UPDATE_MANAGER.update_all_1()

    def update_30_fps(self,dt) :
        self.update_streem()
        
    def update_60_fps(self,dt) :
        """main_loop avec toutes les updates"""
        self.update_notif()
        UPDATE_MANAGER.update_all_all_frame()
        
    
    def update_streem(self) :
        """update les images 30 fois par seconde et l'affiche sur le self.curent_screen.background qui est une image stocké dans box_background"""
        if self.sm.current_screen.streamable :
            if self.dm.is_connected:
                self.sm.current_screen.image_streem = self.dm.get_image(self.sm.current_screen.image_streem)
            else : self.connect_drone()


    def update_notif(self) :
        """prend tout NOTIF_MANAGER.Waiting_notifications et les affiches sur le sm.curent_screen"""
        W_N = NOTIF_MANAGER.Waiting_notifications 
        for k in W_N.keys() :
            for i in W_N[k].keys() : 
                if W_N[k][i] :
                    self.sm.current_screen.notifications[k][i].start_anim()
                    W_N[k][i] = False
            
    def connect_drone(self)->bool :
        if is_wifi_drones_connected() :
            return self.dm.connect()
        return False

class UiScreen(Better_Screen):
    """setup un peu cocase pour avoir un kv.uix.screen et kv.uix.pagelayout"""
    
    def __init__(self, **kwargs):
        
        super(UiScreen, self).__init__(**kwargs)

        pages = UI(ui_screen=self)
    
        self.add_widget(pages)
        #adding notif
        for list_value in self.notifications.values() :
            for notif in list_value :
                self.add_widget(notif)
    """  """
    def go_to(self,value,name_of_the_target_screen:str):
        self.manager.current = name_of_the_target_screen

# -- les mains pages de l'app -- #
class UI(PageLayout):
    def __init__(self,ui_screen,**kwargs):
        self.ui_screen = ui_screen  # Stocker une référence à UiScreen
        super(UI, self).__init__(**kwargs)
        
        self.page1 = Accueil(ui_screen=ui_screen)
        self.page2 = Menue(ui_screen=ui_screen)
        
        self.add_widget(self.page1)
        self.add_widget(self.page2)

class Screen_proj(Better_Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        img_bg= Image(source="image/affiche_project_drone.jpg")
        menue_button = Button(text="", font_size=11, color=(0 ,0 ,0), size_hint=(None,None), size=(80,80), pos_hint={"center_x":0.1,"center_y":0.9}, background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png", size=menue_button.size, pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue, size=self.update_bg, pos=self.update_bg)
        self.add_widget(img_bg)
        self.add_widget(menue_button)

    def go_to_menue(self,value) :
        self.manager.current = "ui"


# ------ Screen_sous_menue  ------ #
class Screen_Controles(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_controles_bg.png")
        img_tuto_mannette = Image(source="CodePython/application/image/tuto_manette.png",pos_hint={"center_x":0.5,"center_y":0.4})
        box_tuto_manette = BoxLayout(pos_hint={"center_x": 0.5,"center_y": 0.5}, size_hint = (None, None), size = (Window.size[0]*0.7, Window.size[1]*0.7))
        box_tuto_manette.add_widget(img_tuto_mannette)
        super().__init__(**kwargs, id_text_titre="app.text_title.controles", icone=icone, background=None)

        self.add_widget(box_tuto_manette)



class Screen_Classique(Screen_Stramable) :
    def __init__(self,**kwargs):
        #icone = Image(source="image/icone_button_classique_bg.png")
        super().__init__(**kwargs)
        box_contol = FloatLayout()
        joy_r = Joystick(size_hint=(1.0/3.0, 1.0/3.0), pos_hint={"center_x":0.3,"center_y":0.7})
        joy_l = Joystick(size_hint=(1.0/3.0, 1.0/3.0), pos_hint={"center_x":0.3,"center_y":0.3})
        box_contol.add_widget(joy_r)
        box_contol.add_widget(joy_l)
        
        

        self.add_widget(box_contol)


class Screen_Automatique(Screen_Stramable) :
    def __init__(self,**kwargs):

        super().__init__(**kwargs)

        

if __name__ == "__main__" :
    Config.set('kivy', 'window_icon', 'CodePython/application/image/logo_drone_aid.ico')
    The_app().run()