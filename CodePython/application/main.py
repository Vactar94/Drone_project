from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager,RiseInTransition
from code_python.notification import Notification, crea_notif
from kivy.clock import Clock
from code_python.global_function import det_sys
from code_python.better_Kivy import Better_Screen, Screen_sous_menu
from code_python.menue import Menue
from code_python.accueil import Accueil
from code_python.telo import DRONE
from code_python.notification import NOTIF_MANAGER



Window.size = [360, 620]
Window.OS = det_sys()




class The_app(App):
    """
    la main_app a partir du quel l'app se lance
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=RiseInTransition())
        self.dm = DRONE
        self.task = None



    def build(self):
        
        #création des screens  
        notifs = crea_notif()
        ui_screen = UiScreen(name='ui', notifications=notifs.copy())
        controle_screen = Screen_Controles(name='controles', notifications=notifs.copy())
        antipersonelle_screen = Screen_Antipersonelle(name="antipersonelle", notifications=notifs.copy())
        classique_screen = Screen_Classique(name="classique", notifications=notifs.copy())
        automatique_screen = Screen_Automatique(name="automatique", notifications=notifs.copy())
        screen_affiche = Screen_proj(name="affiche", notifications=notifs.copy())

        # ajout des screens au screen manager

        self.sm.add_widget(ui_screen)
        self.sm.add_widget(classique_screen)
        self.sm.add_widget(screen_affiche)
        self.sm.add_widget(controle_screen)
        self.sm.add_widget(antipersonelle_screen)
        self.sm.add_widget(automatique_screen)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        
        return self.sm
    
    def update(self,dt) :
        """main_loop avec toutes les updates"""
        self.update_notif()
        self.update_streem()
        
    
    def update_streem(self) :
        if self.sm.current_screen.streem_background :
            if self.dm.is_connected:
                self.sm.current_screen.background = self.dm.get_image()
            else : self.connect_drone()


    def update_notif(self) :
        print(self.sm.current_screen)
        W_N = NOTIF_MANAGER.Waiting_notifications 
        for k in W_N.keys() :
            for i in W_N[k].keys() : 
                if W_N[k][i] :
                    self.sm.current_screen.notifications[k][i].start_anim()
                    W_N[k][i] = False
            
    def connect_drone(self) :
        return self.dm.connect()

class UiScreen(Better_Screen):
    
    def __init__(self, **kwargs):
        
        super(UiScreen, self).__init__(**kwargs)

        pages = UI(ui_screen=self)
    
        self.add_widget(pages)
        #adding notif
        for k in self.notifications.keys() :
            for notif in self.notifications[k] :
                print(notif)
                self.add_widget(notif)
    
        

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
        img_background = Image(source="CodePython/application/image/tuto_manette.png",pos_hint={"center_x":0.5,"center_y":0.4})
        background = BoxLayout()

        background.add_widget(img_background)

        super().__init__(**kwargs, text_titre="Controles", icone=icone, background=background, streem_background=False)
        self.add_widget(self.redu_layout)
        self.add_widget(self.background)
        
        
        

class Screen_Antipersonelle(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_antipersonelle_bg.png")
        super().__init__(**kwargs, text_titre="Antipersonnelle", icone=icone, streem_background=True)
        self.add_widget(self.redu_layout)
        self.add_widget(self.background)



class Screen_Classique(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_classique_bg.png")
        super().__init__(**kwargs, text_titre="Classique", icone=icone, streem_background=True)
        self.add_widget(self.redu_layout)
        self.add_widget(self.background)
        

class Screen_Automatique(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_automatique_bg.png")
        super().__init__(**kwargs, text_titre="Automatique", icone=icone, streem_background=True)
        self.add_widget(self.redu_layout)
        self.add_widget(self.background)
        

if __name__ == "__main__" :
    The_app().run()
