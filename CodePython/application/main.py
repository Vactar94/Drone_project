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
    """
    la main_app a partire duquelle tout se lance
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        sm = ScreenManager(transition=RiseInTransition())
        ui_screen = UiScreen(name='ui')
        controle_screen = Screen_Controles(name='controles')
        antipersonelle_screen = Screen_Antipersonelle(name="antipersonelle")
        classique_screen = Screen_Classique(name="classique")
        automatique_screen = Screen_Automatique(name="automatique")
        sm.add_widget(ui_screen)
        sm.add_widget(classique_screen)
        sm.add_widget(controle_screen)
        sm.add_widget(antipersonelle_screen)
        sm.add_widget(automatique_screen)
        
        return sm

# faire en sorte que un page layout soit un screen pour faire en sorte de passer d'une page a l'autre de avec fluidité
class UiScreen(Screen):
    
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
        """
        pas sur de le garder ptet que c'est pas a moi de le faire en tt ca le bouton existe
        """
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

        

# ------------------------ page du menue ------------------------ # 
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

        titre_page = Label(text="Selectionnez votre mode : ",pos_hint={"center_x":0.5,"center_y":0.85},color=(0, 0, 0))

        box_button_classique = layout_bouton_menue(name="classique",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(1/25),self.size[1]*(2/9)))
        box_button_automatique = layout_bouton_menue(name="automatique",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(1/25),self.size[1]*(5/9)))
        box_button_controles = layout_bouton_menue(name="controles",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(2/9),self.size[1]*(2/9)))
        box_button_antipersonelle = layout_bouton_menue(name="antipersonelle",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(2/9),self.size[1]*(5/9)))


        self.add_widget(titre_page)
        self.add_widget(box_button_classique)
        self.add_widget(box_button_automatique)
        self.add_widget(box_button_controles)
        self.add_widget(box_button_antipersonelle)

class layout_bouton_menue(RelativeLayout):

    def __init__(self,name:str='',ui_screen=None, **kw):
        self.ui_screen = ui_screen
        self.name = name
        super().__init__(**kw)
        with self.canvas.before :
            Color(0, 0, 0)
            RoundedRectangle(pos=(0,0),size=self.size,radius=[30,30])
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95),radius=[30,30])
        titre = Label(text=f"\n{name}",pos_hint={"center_x": 0.5, "center_y": 0.0},color=(0, 0, 0))
        button = Button(size=(self.size[0]*0.90,self.size[1]*0.90),size_hint=(None, None),background_color=(0, 0, 0, 0),pos = (self.size[1]*0.05,self.size[1]*0.05))
        with button.canvas.before:
            Color(0, 0, 0)
            button.bg_rect = Image(source=f"image/icone_button_{name}_bg.png",pos=button.pos,size=button.size)
        button.bind(on_release=self.go_to,pos=self.update_bg, size=self.update_bg)
        self.add_widget(titre)
        self.add_widget(button)
    
    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
    
    def go_to(self,value):
        self.ui_screen.go_to(value,self.name)


# ------ layout de des sous menue ------ #
class Screen_sous_menu(Screen) :
        
    def __init__(self, text_titre:str="", icone:Image=None ,**kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.redu_box = RelativeLayout(size=self.size)
        titre = Label(text=text_titre, color=(0, 0, 0), pos_hint={"center_x":0.5,"center_y":0.85})
        with self.redu_box.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(1, 1, 1)
            RoundedRectangle(pos=(self.size[0]*(0.01),self.size[1]*(0.01)),size=(self.size[0]*0.43,self.size[1]*0.98),radius=[50,50])
        menue_button = Button(text="", font_size=11, color=(0 ,0 ,0), size_hint=(None,None), size=(80,80), pos_hint={"center_x":0.1,"center_y":0.9}, background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png",size=menue_button.size,pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue,size=self.update_bg,pos=self.update_bg)
        
        if icone != None :
            icone.pos_hint = {"center_x":0.87,"center_y":0.9}
            icone.size_hint = (None, None)
            icone.size = [50,50]
            self.redu_box.add_widget(icone)
        else : print(f"{titre.text} n'a pas d'icone")

        self.redu_box.add_widget(menue_button)
        self.redu_box.add_widget(titre)
        self.add_widget(self.redu_box)

    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size

    def go_to_menue(self,value) :
        self.manager.current = "ui"

# ------ utilisation ce ceci ------ #
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
