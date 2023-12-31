from kivy.uix.image import Image
from kivy.uix.spinner import Spinner

from code_python.better_Kivy import Screen_sous_menu
from code_python.langues.langues import LANGUES, POSSIBLES_LANGUAGES


class Screen_Parametre(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_parametre_bg.png")
        super().__init__(**kwargs, id_text_titre="app.text_title.parametres", icone=icone)


        # ------------------- button selection langues ------------------- #
        possibles_languages = POSSIBLES_LANGUAGES
        select_language = Spinner(text=possibles_languages[LANGUES.current_language-1], values=possibles_languages, size_hint=(None, None), size=(100, 44),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        def switsh_language(spinner, text):
            LANGUES.current_language = text
            print(f"current_language = {text}")


        select_language.bind(text=switsh_language)

        self.add_widget(select_language)