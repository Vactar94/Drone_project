from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
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
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.image import Image,AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition,CardTransition,FallOutTransition,RiseInTransition,SlideTransition,NoTransition,SwapTransition,WipeTransition
from jnius import autoclass
import time
import pyglet
import platform

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.graphics import Ellipse, Color

class RoundedImage(BoxLayout):
    def __init__(self, source,radius, **kwargs):
        self.orientation="vertical"
        super(RoundedImage, self).__init__(**kwargs)
        
        self.image = AsyncImage(source=source,size=self.size,allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)

        """with self.canvas.before:
            # Créez un masque de coin arrondi pour l'image
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(size=[self.size[0]/2,self.size[1]], pos=self.pos,radius=[radius,radius])
            self.bind(size=self._update_rect, pos=self._update_rect)"""

    def _update_rect(self, instance, value):
        # Mettez à jour la position et la taille du masque de coin arrondi
        self.rect.pos = self.pos

        self.rect.size = self.size




Window.size = [360, 620]

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

    def transition(self, screen_in, screen_out):
        # Si vous souhaitez une transition de gauche à droite
        #animation_in = Animation(x=0, duration=0.5)
        #animation_out = Animation(x=-self.width, duration=0.5) 
        # Si vous souhaitez une transition de droite à gauche
        animation_in = Animation(x=0, duration=0.5)
        animation_out = Animation(x=self.width, duration=0.5)

        animation_in.start(screen_in)
        animation_out.start(screen_out)
        self.current = screen_in.name

class FirstScreen(Screen):
    def __init__(self, **kw):
        self.size = Window.size
        super().__init__(**kw)
        b = Button(text="go to screen 2",size_hint=(None,None),pos_hint={"center_x":0.5,"center_y":0.5})
        b.bind(on_release=self.go_to_screen_2)
        bg = RelativeLayout(size_hint=(None,None),size=self.size)
        rounded_image = RoundedImage(source='image/layout_bg_app_tras_bg.png',size_hint=(None,None),size=self.size,radius=50)
        bg.add_widget(rounded_image)
        self.add_widget(b)
        self.add_widget(bg)
    
    def go_to_screen_2(self,value):
        self.manager.current= "second"


class SecondScreen(Screen):
    def __init__(self, **kw):
        self.size = Window.size
        
        super().__init__(**kw)
        b = Button(text="go to screen 1",size_hint=(None,None),pos_hint={"center_x":0.5,"center_y":0.5})
        b.bind(on_release=self.go_to_screen_1)
        self.add_widget(b)

    def go_to_screen_1(self,value):
        self.manager.current = "first"

class TestApp(App):
    def build(self):
        sm = MyScreenManager(transition=RiseInTransition())
        sm.add_widget(FirstScreen(name="first"))
        sm.add_widget(SecondScreen(name="second"))
        return sm

if __name__ == '__main__':
    TestApp().run()
