from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from code_python.langues.langues import Updatable_Label
from code_python.tello import DRONE
from code_python.notification import NOTIF_MANAGER
from code_python.global_function import is_wifi_drones_connected



class Better_Screen(Screen) :
    
    def __init__(self,notifications : dict = None, **kw):
        
        super().__init__(**kw)
        self.streamable = False


        if notifications != None and type(notifications) != dict:
            print("notification incorrecte il faut passer un dictonnaire enculer ")
            print(notifications.text)
            a = 1+"g"
        else :
            self.notifications = notifications

        
    def update_bg(self,element,value):
        """update les positions des bg de pleins de trucs"""
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
    
    def on_pre_enter(self,*args) :
        return super().on_pre_enter(*args)

    def on_pre_leave(self, *args):
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

class Screen_sous_menu(Better_Screen) :
        
    def __init__(self, id_text_titre:str="", icone:Image=None ,background:BoxLayout=None, name_screen_target_return_button:str="ui",**kwargs):
        
        super().__init__(**kwargs)
        self._target_retrun_button = name_screen_target_return_button
        self.size = Window.size

        if type(background) == BoxLayout :
            self.add_widget(background)

        self.rendu_layout = RelativeLayout(size=self.size)
        
        titre = Updatable_Label(id_text=id_text_titre, color=(0, 0, 0), pos_hint={"center_x":0.5,"center_y":0.85},font_size_type="titre")

        with self.rendu_layout.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(1, 1, 1)
            RoundedRectangle(pos=(self.size[0]*(0.01),self.size[1]*(0.01)),size=(self.size[0]*0.43,self.size[1]*0.98),radius=[50,50])
        
        menue_button = Button(text="", color=(0 ,0 ,0), size_hint=(None,None), size=(60,60), pos_hint={"center_x":1-0.87,"center_y":0.9}, background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png",size=menue_button.size,pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue,size=self.update_bg,pos=self.update_bg)
        
        if icone != None :
            icone.pos_hint = {"center_x":0.87,"center_y":0.9}
            icone.size_hint = (None, None)
            icone.size = [50,50]
            self.rendu_layout.add_widget(icone)
        else : print(f"{titre.text} n'a pas d'icone")
        
        self.rendu_layout.add_widget(menue_button)
        self.rendu_layout.add_widget(titre)
        self.add_widget(self.rendu_layout)
        


    def go_to_menue(self,value) :
        self.manager.current = self._target_retrun_button
    


def creat_layout_button_menu(name, ui_screen, size_hint, pos_hint) :
    button =  Layout_bouton_menue(name=name, ui_screen=ui_screen, buttton_size_hint=size_hint, button_pos_hint=pos_hint)
    return button


class Layout_bouton_menue(FloatLayout):

    def __init__(self ,name:str='',ui_screen=None, button_pos_hint={}, buttton_size_hint=(), **kw):
        self.ui_screen = ui_screen
        self.name = name
        super().__init__(**kw)

        button = Button(size_hint=buttton_size_hint,background_color=(0, 0, 0, 0), pos_hint=button_pos_hint)
        print(f"size button : {button.size}")
        with button.canvas.before:
            Color(0, 0, 0)
            button.bg_rect = Image(source=f"image/icone_button_{name}_bg.png", pos=button.pos, size=button.size)
        button.bind(on_release=self.go_to,pos=self.update_bg, size=self.update_bg)
        print(button.pos_hint)
        print(button_pos_hint)
        pos_hint_titre = {"center_x":button_pos_hint["center_x"], "center_y":button_pos_hint["center_y"]-0.1}
        titre = Updatable_Label(id_text=f"app.menue.button.{name}",pos_hint=pos_hint_titre,color=(0, 0, 0))

        self.add_widget(titre) 
        self.add_widget(button)
    
    def update_bg(self,element,value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
    
    def go_to(self,value):
        self.ui_screen.go_to(value,self.name)


