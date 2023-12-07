from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
import threading

from code_python.better_Kivy import RoundedImage
from code_python.global_function import is_drones_connected, is_controller_connected

class Accueil(RelativeLayout) :
    n=0
    def __init__(self,ui_screen,notif:dict,**kwargs):
        self.ui_screen = ui_screen
        super().__init__(**kwargs)
        self.notifications = notif
        self.size = Window.size
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95),radius=[30,30])
            Color(0,0,0)
            Rectangle(pos=(self.size[0]//13 ,0),size=(self.size[0]//100,self.size[1]))
            
        RoundedImage(image_source="image/layout_bg_app.png",radius=[30,30],pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95))
        
        desctiption = Button(text="desctiption \nde \nl'app \net \ndu \nprojet",pos_hint={"center_x":0.5,"center_y":0.6},color=(0,0,0),background_color=(0,0,0,0),size_hint=(None,None))
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




        self.add_widget(conectivity_drone)
        self.add_widget(conectivity_contoler)
        self.add_widget(credit)
        self.add_widget(titre)
        self.add_widget(desctiption)
        


    def drone_conectivity(self,button):
        if is_drones_connected() : v = 1
        else : v = 0
        self.notifications["D"][v].anim.start(self.notifications["D"][v])
        

    def go_to_affiche(self,value):
        self.ui_screen.go_to(value,"affiche")

    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
         
    def mannette_conectivity_statue(self, dt) :
        self.conectivity_drone.disabled = False
        value = int()
        self.notifications["M"][value].anim.start(self.notifications["M"][value])

    def mannette_conectivity(self,button:Button):
        """
        pas sur de le garder ptet que c'est pas a moi de le faire en tt ca le bouton existe
        """
        self.conectivity_drone.disabled = True
        
        threading.Thread(target=is_controller_connected)
        
