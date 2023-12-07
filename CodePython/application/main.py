from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager,RiseInTransition
from code_python.notification import Notification, crea_notif

from code_python.global_function import det_sys
from code_python.better_Kivy import Better_Screen, Screen_sous_menu
from code_python.menue import Menue
from code_python.accueil import Accueil


Window.size = [360, 620]
Window.OS = det_sys()




class The_app(App):
    """
    la main_app a partir du quel l'app se lance
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        sm = ScreenManager(transition=RiseInTransition())

        #création des screens  

        ui_screen = UiScreen(name='ui')
        controle_screen = Screen_Controles(name='controles')
        antipersonelle_screen = Screen_Antipersonelle(name="antipersonelle")
        classique_screen = Screen_Classique(name="classique")
        automatique_screen = Screen_Automatique(name="automatique")
        screen_affiche = Screen_proj(name="affiche")

        # ajout des screens au screen manager

        sm.add_widget(ui_screen)
        sm.add_widget(classique_screen)
        sm.add_widget(screen_affiche)
        sm.add_widget(controle_screen)
        sm.add_widget(antipersonelle_screen)
        sm.add_widget(automatique_screen)
        
        return sm
    


class UiScreen(Better_Screen):
    
    def __init__(self, **kwargs):
        
        super(UiScreen, self).__init__(**kwargs)
        pages = UI(ui_screen=self)
        self.add_widget(pages)

    def go_to(self,value,name_of_the_target_screen:str):
        self.manager.current = name_of_the_target_screen


# -- les mains pages de l'app -- #
class UI(PageLayout):
    def __init__(self,ui_screen, **kwargs):
        self.ui_screen = ui_screen  # Stocker une référence à UiScreen
        super(UI, self).__init__(**kwargs)
        notifications = crea_notif([2,2])

        self.page1 = Accueil(ui_screen=ui_screen,notif=notifications)
        self.page2 = Menue(ui_screen=ui_screen, notif=notifications)

        self.add_widget(self.page1)
        self.add_widget(self.page2)





class Screen_proj(Better_Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        img_bg= Image(source="image/affiche_project_drone.jpg")
        menue_button = Button(text="", font_size=11, color=(0 ,0 ,0), size_hint=(None,None), size=(80,80), pos_hint={"center_x":0.1,"center_y":0.9}, background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png",size=menue_button.size,pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue,size=self.update_bg,pos=self.update_bg)
        self.add_widget(img_bg)
        self.add_widget(menue_button)

    def go_to_menue(self,value) :
        self.manager.current = "ui"



# ------ Screen_sous_menue  ------ #
class Screen_Controles(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_controles_bg.png")
        super().__init__(**kwargs,text_titre="Controles",icone=icone)
        

class Screen_Antipersonelle(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_antipersonelle_bg.png")
        super().__init__(**kwargs,text_titre="Antipersonnelle",icone=icone)


class Screen_Classique(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_classique_bg.png")
        super().__init__(**kwargs,text_titre="Classique",icone=icone)
        

class Screen_Automatique(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_automatique_bg.png")
        super().__init__(**kwargs,text_titre="Automatique",icone=icone)
        

if __name__ == "__main__" :
    The_app().run()
