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
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.animation import Animation,AnimationTransition


Window.size = [360, 620]




class Notification (BoxLayout) : 

    def __init__(self,text,duration:int=2,layout:list[int,int]=[1,1],**kwargs) -> None:
        self.name = text
        super().__init__(**kwargs)
        self.layout_max = layout[1]-1
        self.layout_act = layout[0]-1

        self.size = [Window.size[0]//3,Window.size[1]*(0.1)]
        self.size_hint = (None,None)
        self.pos_hint = {"center_y":0.85}
        self.neutral_x = -(self.size[0]+1.2*self.size[0]*self.layout_act)
        self.pos[0] = self.neutral_x

        with self.canvas.before :
            Color (0, 0, 0, 0.3)
            self.bg_rect_ombre = RoundedRectangle(size = self.size, pos = [self.pos[0] - self.size[0]//25, self.pos[1] - self.size[1]//15], radius = [10,10])
            Color (1, 1, 1)
            self.bg_rect = RoundedRectangle(size = self.size,pos = self.pos, radius = [10,10])
        text = Label(text=text,color=(0, 0, 0))


        self.bind(pos=self.update_bg, size=self.update_bg)
        


        self.anim = Animation(x=self.size[0]*0.2 - 1.2*self.size[0]*self.layout_act, duration=duration,transition="out_quint")
        self.anim += Animation(x=self.size[0]*1.5 - 1.2*self.size[0]*self.layout_act, duration=duration,transition="in_quint")
        self.anim.bind(on_complete=self.anim_completed)


        self.add_widget(text)
    
    def __str__(self) -> str:
        return self.name

    def update_bg(self,element,value):
    

        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size

        element.bg_rect_ombre.pos = [element.pos[0] - element.size[0]//15,element.pos[1] - element.size[1]//15]
        element.bg_rect_ombre.size = element.size

    def anim_completed(self,anim, widget) :
        self.pos_hint = {"center_y":0.85}
        self.pos[0] = self.neutral_x

    def start_anim(self) :
        self.anim.start(self)

def crea_notif(layout:list[int,int]=[1, 1],duration:int=1) -> dict[str:list[Notification]] :
        """
            crée un dictonnaire avec avec le type de information en clefs et en valeurs une une list avec en 0 que l'inforamtion est vrai et l'autre que l'information est fausse
            layout[layout_max, curent_layout]
        """
        dict_notif = {}
        dict_notif["M"] =   [Notification("Mannette non connectée", duration=duration, layout=layout), Notification("Mannette connectée",duration=duration,layout=layout)]
        dict_notif["D"] =   [Notification("Drône non connecté", duration=duration, layout=layout), Notification("Drône connecté",duration=duration,layout=layout)]
        return dict_notif

    
class Notif_Manager() :
    
    _Waiting_notifications = {"M":{0:0,1:0},"D":{0:0,1:0}}#ici on créé un dirctionnaire avec en clefs le nom de la notif, et en valuers un dirctionnaire avec en celfs la valeurs de la notif et en valeurs si il faut envoyer la notif ou pas dans la prochiane frame (True or False)
    @property
    def Waiting_notifications(self) :
        """{"lettre de la notif":{0(non):value(True/False), 1(oui):value(True/False)}}"""
        return self._Waiting_notifications
    
    def put_notification(self, screen:Screen=None, waiting_frames:int=0) : 
        pass

NOTIF_MANAGER = Notif_Manager()


if __name__ == "__main__" :
    class test_app(App) :
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
        
        def build(self) :
            notif_box = Notification("mannette non connecté")
            app_box = n_Box_layout(size = Window.size)
            app_box.add_widget(notif_box)

            button = Button(text='Cliquez-moi !',size_hint=(None, None))
            button.bind(on_press=lambda instance: notif_box.start_anim())
            app_box.add_widget(button)
            
            return app_box

    class n_Box_layout(BoxLayout) :
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas.before :
                Color (1,0,0.96)
                Rectangle (size = self.size)

    test_app().run()