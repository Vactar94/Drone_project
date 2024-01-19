from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from code_python.better_Kivy import Better_Screen, Rectangle_hint, RoundedRectangle_hint
from code_python.langues.langues import Updatable_Label

class Screen_sous_menu(Better_Screen) :
        
    def __init__(self, id_text_titre:str="", icone:Image=None ,background:BoxLayout=None, name_screen_target_return_button:str="ui",**kwargs):
        
        super().__init__(**kwargs)
        self._target_retrun_button = name_screen_target_return_button
        self.size = Window.size

        if type(background) == BoxLayout :
            self.add_widget(background)

        self.rendu_layout = FloatLayout(size=self.size)
        
        titre = Updatable_Label(id_text=id_text_titre, color=(0, 0, 0), pos_hint={"center_x":0.5,"center_y":0.85},font_size_type="titre")
        roud_rectangle_blanc = RoundedRectangle_hint(color=(1, 1, 1, 1), radius=[50, 50], pos_hint={"center_x":0.5,"center_y":0.5}, size_hint=(0.9, 0.9))

        rectangle_fond = Rectangle_hint(color=(0, 0, 0, 1),size_hint=(1, 1),pos_hint={"center_x":0.5,"center_y":0.5})

        
        
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
        
        self.rendu_layout.add_widget(rectangle_fond)
        self.rendu_layout.add_widget(roud_rectangle_blanc)
        self.rendu_layout.add_widget(menue_button)
        self.rendu_layout.add_widget(titre)
        self.add_widget(self.rendu_layout)
        


    def go_to_menue(self,value) :
        self.manager.current = self._target_retrun_button
    