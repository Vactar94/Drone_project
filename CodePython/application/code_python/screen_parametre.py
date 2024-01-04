from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from code_python.better_Kivy import Screen_sous_menu
from code_python.langues.langues import LANGUES, Updatable_Spinner, PARAMETRE


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
            
        list_tailles_polices = ["app.parametre.font_size.petit", "app.parametre.font_size.moyen", "app.parametre.font_size.grand"]

        select_font_size = Updatable_Spinner(id_text=list_tailles_polices[1], id_values=list_tailles_polices, size_hint=(None, None), size=(100, 44), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        def switsh_font_size(spinner, text):
            PARAMETRE.switsh_font_size(text)
            print(f"select_font_size = {text}")
        select_font_size.bind(text=switsh_font_size)



        # - add widgets - #
        self.add_widget(select_language)
        self.add_widget(select_font_size)