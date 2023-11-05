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
        super().__init__(**kw)
        b = Button(text="go to screen 2")
        b.bind(on_release=self.go_to_screen_2)
        self.add_widget(b)
    
    def go_to_screen_2(self,value):
        self.manager.current= "second"


class SecondScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        b = Button(text="go to screen 1")
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
