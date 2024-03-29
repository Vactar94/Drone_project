from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from code_python.screen.screen_sous_menu import Screen_sous_menu

from code_python.langues.langues import Update_Image


class Screen_Controles(Screen_sous_menu):
    def __init__(self, **kwargs):
        icone = Image(source="image/icone_button_controles_bg.png")

        img_tuto_mannette = Image(source="image/tuto_manette.png",pos_hint={"center_x":0.5,"center_y":0.4})
        box_tuto_manette = BoxLayout(pos_hint={"center_x": 0.5,"center_y": 0.5}, size_hint = (None, None), size = (Window.size[0]*0.7, Window.size[1]*0.7))
        box_tuto_manette.add_widget(img_tuto_mannette)

        super().__init__(**kwargs, id_text_titre="app.text_title.controles", icone=icone, background=None)

        tuto_manette = Update_Image(id_source="app.control.image.source", pos_hint={"center_x": 0.5, "center_y": 0.4},)

        self.add_widget(tuto_manette)
