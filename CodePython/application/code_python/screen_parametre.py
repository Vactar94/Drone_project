from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from code_python.better_Kivy import Screen_sous_menu
from code_python.langues.langues import LANGUES, Langues, Updatable_Label, Updatable_Spinner, PARAMETRE


class Screen_Parametre(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_parametre_bg.png")
        super().__init__(**kwargs, id_text_titre="app.text_title.parametres", icone=icone)


        # ------------------- button selection langues ------------------- #
        possibles_languages = LANGUES.POSSIBLES_LANGUAGES

        box_lang = FloatLayout(pos_hint={"center_x":0.5, "center_y":0.7})

        titre_lang = Updatable_Label(id_text="app.parametre.lang.titre", pos_hint={"center_x":0.3, "center_y":0.5},color=(0, 0, 0, 1))
        
        select_lang = Spinner(text=possibles_languages[0], values=possibles_languages, size_hint=(None, None), size=(100, 35),pos_hint={'center_x': 0.7, 'center_y': 0.5}, background_color=(0, 0, 0, 0),color=(0, 0, 0, 1))
        
        def switsh_language(spinner, text):
            LANGUES.current_language = text
            print(f"current_language = {text}")
        select_lang.bind(text=switsh_language)

        box_lang.add_widget(titre_lang)
        box_lang.add_widget(select_lang)

        # ------------------- button selection taille police ------------------- #
        box_polices = FloatLayout(pos_hint={"center_x":0.5, "center_y":0.5})
        titre_polices = Updatable_Label(id_text="app.parametre.font_size.titre", pos_hint={"center_x":0.3, "center_y":0.5},color=(0, 0, 0, 1))
            
        list_tailles_polices = ["app.parametre.font_size.petit", "app.parametre.font_size.moyen", "app.parametre.font_size.grand"]
    
        select_font_size = Updatable_Spinner(id_text=list_tailles_polices[1], id_values=list_tailles_polices, pos_hint={'center_x': 0.7, 'center_y': 0.5}, size_hint=(None, None), size=(100, 35), background_color=(0, 0, 0, 0),color=(0, 0, 0, 1))
        def switsh_font_size(spinner, text):
            print(f"enter Parametre.switsh_font_size({text})")
            PARAMETRE.switsh_font_size(text)
            
            print(f"sortie Parametre.switsh_font_size({text})")

            id_text = LANGUES.contre_trad(text)
            if type(id_text) == str :
                spinner.id_text = id_text # permet d'assigné la bonne id en fonction de la value séléctionné dans l'app.
            else :
                print(f"id_text = {id_text} regarder dans screen parametre il y a une erreur")
                a = "a"+1

        select_font_size.bind(text=switsh_font_size)

        box_polices.add_widget(titre_polices)
        box_polices.add_widget(select_font_size)



        # - add widgets - #
        self.add_widget(box_lang)
        self.add_widget(box_polices)