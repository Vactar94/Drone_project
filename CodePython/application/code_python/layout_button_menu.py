from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color

from code_python.langues.langues import Updatable_Label

class Layout_bouton_menue(FloatLayout):

    def __init__(self ,name:str='',ui_screen=None, button_pos_hint={}, buttton_size_hint=(), **kw):
        self.ui_screen = ui_screen
        self.name = name
        super().__init__(**kw)

        button = Button(size_hint=buttton_size_hint,background_color=(0, 0, 0, 0), pos_hint=button_pos_hint, font_name="Georgia.ttf")
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

def creat_layout_button_menu(name, ui_screen, size_hint, pos_hint) :
    button =  Layout_bouton_menue(name=name, ui_screen=ui_screen, buttton_size_hint=size_hint, button_pos_hint=pos_hint)
    return button
