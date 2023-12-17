from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from code_python.telo import DRONE
from code_python.notification import NOTIF_MANAGER




class Better_Screen(Screen) :
    
    def __init__(self,notifications : dict = None,streem_background:bool=False , **kw):
        
        super().__init__(**kw)
        self.streem_background = streem_background
        
        self.background = Image()

        if notifications != None and type(notifications) != dict:
            print("notification incorrecte il faut passer un dictonnaire enculer ")
            print(notifications.text)
            a = 1+"g"
        else :
            self.notifications = notifications


            

    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
    
    def on_pre_enter(self) :

        if self.streem_background :
            if not DRONE.start_streeming() :
                self.go_to_menue("pute")
                NOTIF_MANAGER.Waiting_notifications["D"][0] = True

    def on_pre_leave(self, *args):

        if self.streem_background and DRONE.is_connected:
            DRONE.stop_streeming()
        return super().on_pre_leave(*args)
    
    def __str__(self) :
        return self.name

class RoundedImage(Widget):
    def __init__(self, image_source:str, radius:list[int,int], **kwargs):
        self.image = Image(source=image_source, allow_stretch=True, keep_ratio=False)
        super(RoundedImage, self).__init__(**kwargs)
        
        self.add_widget(self.image)

        self.radius = radius

    def on_size(self, instance, value):
        self.image.size = self.size
        self.image.pos = self.pos

    def on_pos(self, instance, value):
        self.image.pos = value


class Screen_sous_menu(Better_Screen) :
        
    def __init__(self, text_titre:str="", icone:Image=None ,background:BoxLayout=None,**kwargs):
        
        super().__init__(**kwargs)
        if background != None :
            self.background = background
        else : self.background = BoxLayout()
        print(self.background)
        self.size = Window.size
        self.redu_layout = RelativeLayout(size=self.size)
        titre = Label(text=text_titre, color=(0, 0, 0), pos_hint={"center_x":0.5,"center_y":0.85})
        with self.redu_layout.canvas.before:
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
            self.redu_layout.add_widget(icone)
        else : print(f"{titre.text} n'a pas d'icone")
        self.redu_layout.add_widget(menue_button)
        self.redu_layout.add_widget(titre)
        


    def go_to_menue(self,value) :

        self.manager.current = "ui"
    


class Layout_bouton_menue(RelativeLayout):

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