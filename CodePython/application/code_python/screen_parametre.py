from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from code_python.better_Kivy import Screen_sous_menu
from code_python.langues.langues import LANGUES


class Screen_Parametre(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_parametre_bg.png")
        super().__init__(**kwargs, id_text_titre="app.text_title.parametres", icone=icone)


        # ------------------- button selection langues ------------------- #
        possibles_languages = LANGUES.POSSIBLES_LANGUAGES
        select_language = Spinner(text=possibles_languages[0], values=possibles_languages, size_hint=(None, None), size=(100, 44),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        def switsh_language(spinner, text):
            LANGUES.current_language = text
            print(f"current_language = {text}")
        select_language.bind(text=switsh_language)

        # ------------------- button selection taille police ------------------- #
        box_polices = BoxLayout()
            
        list_tailles_polices = []

        select_language = Spinner(text=list_tailles_polices[0], values=list_tailles_polices, size_hint=(None, None), size=(100, 44), pos_hint={'center_x': 0.5, 'center_y': 0.6}, background_color=(0, 0, 0, 0))
        



        # - add widgets - #
        self.add_widget(select_language)