from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


from code_python.better_Kivy import Screen_sous_menu
from code_python.langues.langues import LANGUES, Updatable_Button, Updatable_Label, Updatable_Spinner, PARAMETRE


class Screen_Parametre(Screen_sous_menu) :
    def __init__(self,**kwargs):
        icone = Image(source="image/icone_button_parametre_bg.png")
        super().__init__(**kwargs, id_text_titre="app.text_title.parametres", icone=icone)


        # ------------------- button selection langues ------------------- #
        possibles_languages = LANGUES.POSSIBLES_LANGUAGES

        box_lang = FloatLayout(pos_hint={"center_x":0.5, "center_y":0.55})

        titre_lang = Updatable_Label(id_text="app.parametre.lang.titre", pos_hint={"center_x":0.3, "center_y":0.5},color=(0, 0, 0, 1))
        
        select_lang = Updatable_Spinner(text=possibles_languages[0], values=possibles_languages, size_hint=(None, None), size=(100, 35),pos_hint={'center_x': 0.7, 'center_y': 0.5}, 
                                        background_color=(0, 0, 0, 0),color=(0, 0, 0, 1),update_lang=False)
        
        def switsh_language(spinner, text):
            LANGUES.current_language = text
            print(f"current_language = {text}")
        select_lang.bind(text=switsh_language)

        box_lang.add_widget(titre_lang)
        box_lang.add_widget(select_lang)

        # ------------------- button selection taille police ------------------- #

        pos_hint_button_switsh_font = {"center_x":0.5, "center_y":0.4}# Position du button_switsh size
        box_polices = FloatLayout(pos_hint=pos_hint_button_switsh_font)
        titre_polices = Updatable_Label(id_text="app.parametre.font_size.titre", pos_hint={"center_x":0.3, "center_y":0.5},color=(0, 0, 0, 1))
            
        list_tailles_polices = ["app.parametre.font_size.petit", "app.parametre.font_size.moyen", "app.parametre.font_size.grand"]
    
        select_font_size = Updatable_Spinner(id_text=list_tailles_polices[1], id_values=list_tailles_polices, pos_hint={'center_x': 0.7, 'center_y': 0.5}, size_hint=(None, None), size=(100, 35), background_color=(0, 0, 0, 0),color=(0, 0, 0, 1))
        
        def switsh_font_size(spinner, text):
            PARAMETRE.switsh_font_size(text)
            id_text = LANGUES.contre_trad(text)
            if type(id_text) == str :
                spinner.id_text = id_text # permet d'assigné la bonne id en fonction de la value séléctionné dans l'app.
            else :
                print(f"id_text = {id_text} regardez dans screen parametre il y a une erreur")
                a = "a"+1
        select_font_size.bind(text=switsh_font_size)

        box_polices.add_widget(titre_polices)
        box_polices.add_widget(select_font_size)

        # ------------------- bouton d'accès au screen des parametres du drone ------------------- #
        pos_hint_button_para_drone = {"center_x": 0.5,"center_y" : 0.7}

        box_para_drone = FloatLayout(pos_hint=pos_hint_button_para_drone)
        button_para_drone = Updatable_Button(id_text="app.parametre.info_drone.button", pos_hint={"center_x":0.5, "center_y":0.5}, color=(0, 0, 0, 1), background_color=(0, 0, 0, 0), size_hint=(1.0/2.0, 1.0/20.0))
        button_para_drone.bind(on_release=self.go_to_info_drone)
        box_para_drone.add_widget(button_para_drone)

        
        # - add widgets - #
        self.add_widget(box_para_drone)
        self.add_widget(box_lang)
        self.add_widget(box_polices)
    

    def go_to_info_drone(self, button) : 
        self.manager.current = "info_drone"