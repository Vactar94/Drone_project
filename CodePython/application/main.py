from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty,BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window,WindowBase
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.image import Image,AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen,RiseInTransition
from jnius import autoclass
import pyglet
import platform




def det_sys():
    """determine dans quelle OS on est return la première lettre de l'os :
        W : Windows
        L : Linux
        M : MacOs
        A : Android
        Z : OS non reconue
    """

    system = platform.system()  # Récupère le nom du système d'exploitation
    release = platform.release()  # Récupère la version du système d'exploitation

    print(f"Système d'exploitation : {system}")
    print(f"Version : {release}")

    if system == "Windows":                                                         return "W"
    elif system == "Linux":                                                         return "L"
    elif system == "Darwin":                                                        return "M"
    elif platform.system() == "Linux" and "android" in platform.platform().lower(): return "A"
    else :                                                                          return "Z"


def check_controller_connectivity():
    if Window.OS == "A" :
        InputDevice = autoclass('android.view.InputDevice')
        input_devices = InputDevice.getDeviceIds()
        for device_id in input_devices:
            device = InputDevice.getDevice(device_id)
            if device.getSources() & InputDevice.SOURCE_GAMEPAD:
                return True
        return False
    elif Window.OS == "W" :
        pyglet.options["audio"] = ("pulse", "openal", "silent")
        pyglet.options["debug_media"] = True
        return len(pyglet.input.get_joysticks())



Window.size = [360, 620]
Window.OS = det_sys()



class The_app(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        sm = ScreenManager(transition=RiseInTransition())
        ui_screen = UiScreen(name='ui')
        controle_screen = Screen_Controles(name='controle')
        antipersonelle_screen = Screen_Antipersonelle(name="antipersonelle")
        classique_screen = Screen_Classique(name="classique")
        automatique_screen = Screen_Automatique(name="automatique")
        sm.add_widget(ui_screen)
        sm.add_widget(classique_screen)
        sm.add_widget(controle_screen)
        sm.add_widget(antipersonelle_screen)
        sm.add_widget(automatique_screen)
        
        return sm

class UiScreen(Screen):
    
    def __init__(self, **kwargs):
        
        super(UiScreen, self).__init__(**kwargs)
        pages = UI(ui_screen=self)
        self.add_widget(pages)

    def go_to_control(self,value):
        self.manager.current = "controle"

    def go_to_antipersonelle(self,value):
        self.manager.current = "antipersonelle"

    def go_to_classique(self,value):
        self.manager.current = "classique"

    def go_to_automatique(self,value):
        self.manager.current = "automatique"


class UI(PageLayout):
    def __init__(self,ui_screen, **kwargs):
        self.ui_screen = ui_screen  # Stocker une référence à UiScreen
        super(UI, self).__init__(**kwargs)
        self.page1 = Accueil()
        self.page2 = Menue(ui_screen=ui_screen)

        self.add_widget(self.page1)
        self.add_widget(self.page2)

    # ------------------ page d'accueil ------------------ #
class Accueil(RelativeLayout) :
    n=0
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95),radius=[30,30])
            Color(0,0,0)
            Rectangle(pos=(self.size[0]//13 ,0),size=(self.size[0]//100,self.size[1]))
        
        desctiption = Label(text="desctiption \nde \nl'app \net \ndu \nprojet",pos_hint={"center_x":0.5,"center_y":0.6},color=(0,0,0))
        credit = Label(text="Crédit :   \nOscar : application \nAdrien : controle du drone ",pos_hint={"center_x":0.6,"center_y":0.2})
        titre = Label(text='[b]Drone Automatik[/b]',size_hint_y=None,color=(1, 1, 1),height=200,pos_hint={"center_x":0.6,"center_y":0.85},font_size=25,markup=True)
        
        #------------- bouton pour passer aux menus -------------#
        button = Button(text="",size_hint=(None,None),size=(80,40),pos_hint={"center_x":0.11,"center_y":0.9},background_color=(0,0,0,0),background_normal="")
        button.bind(pos=self.update_bg, size=self.update_bg)
        with button.canvas.before:
            Color(0, 0, 0)
            button.bg_rect = Image(source="image/bg_menue.png",pos=button.pos,size=button.size)
        button.bind(on_release=self.mannette_conectivity)

        self.add_widget(button)
        self.add_widget(credit)
        self.add_widget(titre)
        self.add_widget(desctiption)



        

    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
         



    def mannette_conectivity(self,value):
        if Window.OS == "A" :
            if check_controller_connectivity() :
                print("ya une mannette")
            else :
                print("ya pas de mannette")
        elif Window.OS == "W" :
            if check_controller_connectivity() == 0 :
                print("il y n'y a pas de mannette conecter")
            elif  check_controller_connectivity() == 1 : 
                print("il y a une mannette ce connecter")
            else :
                print(f"il y a {check_controller_connectivity()} mannettes de conecter ")
        self.n+=1
        print(f"button_appuiller({self.n} eme fois) ")

        



class Menue(RelativeLayout):
    def __init__(self,ui_screen, **kwargs):
        super().__init__(**kwargs)
        self.ui_screen = ui_screen

        self.size = Window.size
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95),radius=[30,30])

        #---------------- Bouton des contoles de la manette ----------------#
        box_button_controles = RelativeLayout(size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(2/9),self.size[1]*(2/9)))
        with box_button_controles.canvas.before :
            Color(0, 0, 0)
            RoundedRectangle(pos=(0,0),size=box_button_controles.size,radius=[30,30])
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(box_button_controles.size[1]*0.025,box_button_controles.size[1]*0.025),size=(box_button_controles.size[0]*0.95,box_button_controles.size[1]*0.95),radius=[30,30])
        titre_button_controles = Label(text="\nContrôles",pos_hint={"center_x": 0.5, "center_y": 0.0},color=(0, 0, 0))
        button_controles = Button(size=(box_button_controles.size[0]*0.90,box_button_controles.size[1]*0.90),size_hint=(None, None),background_color=(0, 0, 0, 0),pos = (box_button_controles.size[1]*0.05,box_button_controles.size[1]*0.05))
        with button_controles.canvas.before:
            Color(0, 0, 0)
            button_controles.bg_rect = Image(source="image/bg_button_controle.png",pos=button_controles.pos,size=button_controles.size)
        button_controles.bind(on_release=self.go_to_control,pos=self.update_bg, size=self.update_bg)
        box_button_controles.add_widget(titre_button_controles)
        box_button_controles.add_widget(button_controles)

        #---------------- Bouton du mode antipersonelle ----------------#
        box_button_antipersonelle = RelativeLayout(size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(2/9),self.size[1]*(5/9)))
        with box_button_antipersonelle.canvas.before :
            Color(0, 0, 0)
            RoundedRectangle(pos=(0,0),size=box_button_antipersonelle.size,radius=[30,30])
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(box_button_antipersonelle.size[1]*0.025,box_button_antipersonelle.size[1]*0.025),size=(box_button_antipersonelle.size[0]*0.95,box_button_antipersonelle.size[1]*0.95),radius=[30,30])
        titre_button_antipersonelle = Label(text="\nMode Antipersonelle",pos_hint={"center_x": 0.5, "center_y": 0.0},color=(0, 0, 0))
        
        button_antipersonelle = Button(size=(box_button_antipersonelle.size[0]*0.90,box_button_antipersonelle.size[1]*0.90),size_hint=(None, None),background_color=(0, 0, 0, 0),pos = (box_button_antipersonelle.size[1]*0.05,box_button_antipersonelle.size[1]*0.05))
        with button_antipersonelle.canvas.before:
            Color(0, 0, 0)
            button_antipersonelle.bg_rect = Image(source="image/bg_antipersonelle.png",pos=button_antipersonelle.pos,size=button_antipersonelle.size)
        button_antipersonelle.bind(on_release=self.go_to_antipersonelle,pos=self.update_bg, size=self.update_bg)
        box_button_antipersonelle.add_widget(titre_button_antipersonelle)
        box_button_antipersonelle.add_widget(button_antipersonelle)

        #---------------- Bouton du mode automatique ----------------#
        box_button_automatique = RelativeLayout(size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(1/25),self.size[1]*(5/9)))
        with box_button_automatique.canvas.before :
            Color(0, 0, 0)
            RoundedRectangle(pos=(0,0),size=box_button_automatique.size,radius=[30,30])
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(box_button_automatique.size[1]*0.025,box_button_automatique.size[1]*0.025),size=(box_button_automatique.size[0]*0.95,box_button_automatique.size[1]*0.95),radius=[30,30])
        titre_button_automatique = Label(text="\nMode Automatique",pos_hint={"center_x": 0.5, "center_y": 0.0},color=(0, 0, 0))
        
        button_button_automatique = Button(size=(box_button_automatique.size[0]*0.90,box_button_automatique.size[1]*0.90),size_hint=(None, None),background_color=(0, 0, 0, 0),pos = (box_button_automatique.size[1]*0.05,box_button_automatique.size[1]*0.05))
        with button_button_automatique.canvas.before:
            Color(0, 0, 0)
            button_button_automatique.bg_rect = Image(source="image/icone_drone_bg.png",pos=button_button_automatique.pos,size=button_button_automatique.size)
        button_button_automatique.bind(on_release=self.go_to_automatique,pos=self.update_bg, size=self.update_bg)
        box_button_automatique.add_widget(titre_button_automatique)
        box_button_automatique.add_widget(button_button_automatique)

        #---------------- Bouton du mode classique ----------------#
        box_button_classique = RelativeLayout(size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(1/25),self.size[1]*(2/9)))
        with box_button_classique.canvas.before :
            Color(0, 0, 0)
            RoundedRectangle(pos=(0,0),size=box_button_classique.size,radius=[30,30])
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(box_button_classique.size[1]*0.025,box_button_classique.size[1]*0.025),size=(box_button_classique.size[0]*0.95,box_button_classique.size[1]*0.95),radius=[30,30])
        titre_button_classique = Label(text="\nMode Classique",pos_hint={"center_x": 0.5, "center_y": 0.0},color=(0, 0, 0))
        
        button_button_classique = Button(size=(box_button_classique.size[0]*0.90,box_button_classique.size[1]*0.90),size_hint=(None, None),background_color=(0, 0, 0, 0),pos = (box_button_classique.size[1]*0.05,box_button_classique.size[1]*0.05))
        with button_button_classique.canvas.before:
            Color(0, 0, 0)
            button_button_classique.bg_rect = Image(source="image/icone_smatrphone_bg.png",pos=button_button_classique.pos,size=button_button_classique.size)
        button_button_classique.bind(on_release=self.go_to_classique,pos=self.update_bg, size=self.update_bg)
        box_button_classique.add_widget(titre_button_classique)
        box_button_classique.add_widget(button_button_classique)


        titre_page = Label(text="Selectionnez votre mode : ",pos_hint={"center_x":0.5,"center_y":0.85},color=(0, 0, 0))

        self.add_widget(titre_page)
        self.add_widget(box_button_classique)
        self.add_widget(box_button_automatique)
        self.add_widget(box_button_controles)
        self.add_widget(box_button_antipersonelle)
    
    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size

    def go_to_control(self,value):
        self.ui_screen.go_to_control(value)

    def go_to_antipersonelle(self,value):
        self.ui_screen.go_to_antipersonelle(value)

    def go_to_classique(self,value):
        self.ui_screen.go_to_classique(value)

    def go_to_automatique(self,value):
        self.ui_screen.go_to_automatique(value)


class Screen_Controles(Screen) :
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        print(self.size)
        self.redu_box = RelativeLayout(size=self.size)
        titre = Label(text="Controles :",color=(0, 0, 0),pos_hint={"center_x":0.5,"center_y":0.85})
        with self.redu_box.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(1, 1, 1)
            RoundedRectangle(pos=(self.size[0]*(0.01),self.size[1]*(0.01)),size=(self.size[0]*0.43,self.size[1]*0.98),radius=[50,50])
        menue_button = Button(text="",font_size=11,color=(0 ,0 ,0),size_hint=(None,None),size=(80,80),pos_hint={"center_x":0.1,"center_y":0.9},background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png",size=menue_button.size,pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue,size=self.update_bg,pos=self.update_bg)
        self.redu_box.add_widget(menue_button)
        self.redu_box.add_widget(titre)
        self.add_widget(self.redu_box)

    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
    
    def go_to_menue(self,value) :
        self.manager.current = "ui"


class Screen_Antipersonelle(Screen) :
    def __init__(self,**kwargs):
            super().__init__(**kwargs)
            with self.canvas.before:
                Color(36/255, 181/255, 11/255)
                Rectangle(pos=(0,Window.size[1]-self.size[1]),size=self.size)
                Color(1, 1, 1)
                Rectangle(pos=(0,self.size[1]//2),size=(self.size[0],self.size[1]//2))
            menue_button = Button(text="Antipersonelle\nretour au menue")
            menue_button.bind(on_release=self.go_to_menue)

            self.add_widget(menue_button)

    def go_to_menue(self,value) :
        self.manager.current = "ui"

class Screen_Classique(Screen) :
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(36/255, 181/255, 11/255)
            Rectangle(pos=(0,Window.size[1]-self.size[1]),size=self.size)
            Color(1, 1, 1)
            Rectangle(pos=(0,self.size[1]//2),size=(self.size[0],self.size[1]//2))
        menue_button = Button(text="Classique\nretour au menue")
        menue_button.bind(on_release=self.go_to_menue)

        self.add_widget(menue_button)

    def go_to_menue(self,value) :
        self.manager.current = "ui"

class Screen_Automatique(Screen) :
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(36/255, 181/255, 11/255)
            Rectangle(pos=(0,Window.size[1]-self.size[1]),size=self.size)
            Color(1, 1, 1)
            Rectangle(pos=(0,self.size[1]//2),size=(self.size[0],self.size[1]//2))
        menue_button = Button(text="Automatique\nretour au menue")
        menue_button.bind(on_release=self.go_to_menue)

        self.add_widget(menue_button)

    def go_to_menue(self,value) :
        self.manager.current = "ui"


if __name__ == "__main__" :
    The_app().run()
