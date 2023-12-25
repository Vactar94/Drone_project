from kivy.uix.image import Image

from code_python.better_Kivy import Screen_sous_menu


class Screen_Parametre(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_parametre_bg.png")
        super().__init__(**kwargs, text_titre="Paramètres", icone=icone)
        