from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
import threading
from code_python.notification import NOTIF_MANAGER
from code_python.telo import DRONE


from code_python.better_Kivy import Updatable_Label, UPDATE_MANAGER
from code_python.global_function import is_wifi_drones_connected, chec_controller_connected

class Accueil(RelativeLayout) :
    n=0
    def __init__(self,ui_screen,**kwargs):
        self._is_controller_connected = None
        self.ui_screen = ui_screen
        super().__init__(**kwargs)
        self.size = Window.size
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95),radius=[30,30])
            Color(0,0,0)
            Rectangle(pos=(self.size[0]//13 ,0),size=(self.size[0]//100,self.size[1]))

        desctiption = Button(text="Notre drone révolutionnaire,\n contrôlé par cet application, \n optimise la gestion des jeux en \nreconnaissant et déplaçant des \néquipements sportifs jusqu'à\n 1,5 kg. Sa navigation \nintelligente et sa stabilité\n exceptionnelle assurent \nun fonctionnement fluide\n et sécurisé. Avec des modes \nmanuels et automatiques, il\n offre une expérience sportive\n dynamique, centralisant \nle travail du personnel.",pos_hint={"center_x":0.6,"center_y":0.56},color=(0,0,0),background_color=(0,0,0,0),size_hint=(None,None))
        desctiption.bind(on_release=self.go_to_affiche)
        credit = Label(text="Crédit :   \nOscar : application \nAdrien : controle du drone ",pos_hint={"center_x":0.6,"center_y":0.2})
        titre = Label(text='[b]Drone Automatik[/b]',size_hint_y=None,color=(1, 1, 1),height=200,pos_hint={"center_x":0.6,"center_y":0.85},font_size=25,markup=True)
        
        #------------- bouton pour connecter mannette  -------------#
        conectivity_contoler = Button(text="",size_hint=(None,None),size=(80,40),pos_hint={"center_x":0.11,"center_y":0.9},background_color=(0,0,0,0),background_normal="")
        conectivity_contoler.bind(pos=self.update_bg, size=self.update_bg)
        with conectivity_contoler.canvas.before:
            Color(0, 0, 0)
            conectivity_contoler.bg_rect = Image(source="image/bg_mannette_menue.png",pos=conectivity_contoler.pos,size=conectivity_contoler.size)
        conectivity_contoler.bind(on_release=self.mannette_conectivity)
        self.conectivity_contoler = conectivity_contoler

        conectivity_drone = Button(text="",size_hint=(None,None),size=(80,40),pos_hint={"center_x":0.11,"center_y":0.1},background_color=(0,0,0,0),background_normal="")
        conectivity_drone.bind(pos=self.update_bg, size=self.update_bg)
        with conectivity_drone.canvas.before:
            Color(0, 0, 0)
            conectivity_drone.bg_rect = Image(source="image/bg_drone_menue.png",pos=conectivity_drone.pos,size=conectivity_drone.size)
        conectivity_drone.bind(on_release=self.drone_conectivity)
        self.conectivity_drone = conectivity_drone


        #batterie_drone = DRONE.get_battery()
        #if batterie_drone >= 0 :
        #    text_batt = "Batterie du drone :"
        #else :
        #    text_batt = "Connectez le drone pour avoir la batterie "
        
        #batterie_drone_label = Updatable_Label(text=text_batt,frequence=1,updating_variable=DRONE.get_battery) pour une futur MAJ ^^
        


        self.add_widget(conectivity_drone)
        self.add_widget(conectivity_contoler)
        self.add_widget(credit)
        self.add_widget(titre)
        self.add_widget(desctiption)
    
    @property
    def is_controller_connected(self) :
        return self._is_controller_connected
    
    @is_controller_connected.setter
    def is_controller_connected(self,value) :
        self._is_controller_connected = value

        if value :
            NOTIF_MANAGER.Waiting_notifications["M"][1] = True
        elif not value : 
            NOTIF_MANAGER.Waiting_notifications["M"][0] = True
        




    def drone_conectivity(self,button):
        if DRONE.connect() : v = 1
        else : v = 0
        NOTIF_MANAGER.Waiting_notifications["D"][v] = True
        

    def go_to_affiche(self,value):
        self.ui_screen.go_to(value,"affiche")

    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
         
    def mannette_conectivity_statue(self, dt) :
        self.conectivity_contoler.disabled = False
        v = int()
        NOTIF_MANAGER.Waiting_notifications["D"][v] = True

    def mannette_conectivity(self,button:Button):
        """
        pas sur de le garder ptet que c'est pas a moi de le faire en tt ca le bouton existe
        """
        self.conectivity_contoler.disabled = True
        
        threading.Thread(target=chec_controller_connected,args=(self.is_controller_connected,))
        
