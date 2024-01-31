import json

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.uix.spinner import Spinner

from code_python.better_Kivy import Better_Button, Better_Label


class Langues():
    POSSIBLES_LANGUAGES = []

    def __init__(self) -> None:
        """
        permet de traduire le texte en plein de langues(2)        
        """
        self._dict_langues = {}
        with open("code_python/langues/lang.json", 'r', encoding='utf-8') as file:
            json_langues_file = json.load(file)
            for Langue in json_langues_file.keys():
                if Langue != "DEFAULT":
                    self.POSSIBLES_LANGUAGES.append(Langue)

                self.dict_langues[Langue] = json_langues_file[Langue]

        self._current_language = list(json_langues_file.keys())[0]

    @property
    def current_language(self):
        return self._current_language

    @current_language.setter
    def current_language(self, value):
        """current langage dans l'application"""
        if type(value) == int:
            self._current_language = list(self.dict_langues.keys())[value]
        elif value in self.dict_langues.keys():
            self._current_language = value
        else:
            print(f"value : {value} qui est entré dans le setter de current_language n'est pas comforme")
            a = 1 + "a"

        UPDATE_MANAGER.update_all_lang()

    @property
    def dict_langues(self):
        return self._dict_langues

    @dict_langues.setter
    def dict_langues(self, value):
        """{id_Langue:{id_écriture:str}}"""
        self._dict_langues = value

    def trad(self, id_ecriture) -> str:
        """transphorme un id_ecriture en str"""
        try:
            if self.dict_langues[self.current_language][id_ecriture] == "":
                return id_ecriture
            else:
                return self.dict_langues[self.current_language][id_ecriture]
        except:
            try:
                return self.dict_langues["DEFAULT"][id_ecriture]
            except:
                return id_ecriture

    def contre_trad(self, text) -> str | list:
        """transphorme un id_ecriture en str si il exsite, sinon fait une erreur"""
        id_text = []

        for key in self.dict_langues[self.current_language].keys():
            if self.dict_langues[self.current_language][key] == text:
                id_text.append(key)

        if len(id_text) == 0:
            return text
        elif len(id_text) == 1:
            return id_text[0]
        else:
            return id_text


LANGUES = Langues()


# -------------------------------------------------- Updatable Obj -------------------------------------------------- #
class Update_Image(FloatLayout):
    """ Update image class for Update the image in terms of App current language"""

    def __init__(self, id_source: str, **kwargs):
        super().__init__(**kwargs)
        self.id_source = id_source
        trad_source = LANGUES.trad(self.id_source)
        self.main_image = Image(source=trad_source, pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.add_widget(self.main_image)

        UPDATE_MANAGER.register_lang(self)

    def update_trad(self):
        self.main_image.source = LANGUES.trad(self.id_source)


class Updatable_font:

    def __init__(self, font_size_type: str) -> None:
        self.font_size_type = font_size_type
        self.update_font_size()
        UPDATE_MANAGER.register_font_size(self)

    def update_font_size(self):
        """met a jour la font_size en fontcion de PARAMETTRE.get_curent_font_size"""
        self.font_size = PARAMETRE.get_curent_font_size(self.font_size_type)


class Updatable_lang:
    """Fusionnable avec tout les Buttons, Label de kivy"""

    def __init__(self, id_text: str) -> None:
        self.id_text = id_text
        self.update_trad()
        UPDATE_MANAGER.register_lang(self)

    def update_trad(self):
        self.text = LANGUES.trad(self.id_text)


class Updatable(Updatable_font, Updatable_lang):
    """fusions des classes Updatable_font et Updatabe_lang"""

    def __init__(self, id_text: str, font_size_type: str = "standard", **kwargs):
        Updatable_font.__init__(self, font_size_type=font_size_type)
        Updatable_lang.__init__(self, id_text)

    def __str__(self):
        return self.text


class Updatable_Spinner(Updatable_font, Spinner):
    """version Updatabe de kivy.uix.Spinner
    id_values : list des id du text des values {str}
    id text : id du text {str}
    update_lang: savoir il deviendra éligible a l'update de la langue {bool}[True]
    font_size_type : {str in ["standard","titre","petit"]}["standard"]
    """

    def __init__(self, id_values: list = [], id_text: str = "", update_lang: bool = True, font_size_type="standard",
                 **kwargs):
        # Appeler le constructeur de la classe mère Updatable_font
        Updatable_font.__init__(self, font_size_type)
        # Appeler le constructeur de la classe mère Spinner
        Spinner.__init__(self, **kwargs)

        if update_lang:
            self.id_values = id_values
            self.id_text = id_text
            self.values = id_values
            self.update_trad()
            UPDATE_MANAGER.register_lang(self)

    def update_trad(self):
        """update les values du spinner en les traduisant"""

        for i in range(len(self.values)):
            self.values[i] = LANGUES.trad(self.id_values[i])

        self.text = LANGUES.trad(self.id_text)

    def __str__(self):
        return f"spinner : {self.values} {self.text}"


class Updatable_Label(Label, Updatable):
    """id_text : id du texte traductible dans le fichier json (le text n'est pas obligé d'etre ajouté) {str}
    """

    def __init__(self, id_text: str, **kwargs):
        Label.__init__(self, id_text=id_text, **kwargs)
        Updatable.__init__(self, id_text, **kwargs)


class Updatable_Button(Better_Button, Updatable):
    """id_text : id du texte traductible dans le fichier json (le text n'est pas obligé d'etre ajouté) {str}
    """

    def __init__(self, id_text: str, angle: int = 0, **kwargs):
        Better_Button.__init__(self, angle=angle, id_text=id_text, **kwargs)
        Updatable.__init__(self, id_text, **kwargs)


class Update_Manager():
    """permet a update des variable contenue dans des object kivy (notament les labels et les buttons)"""
    _obj_update_all_frame = []
    _obj_update_1 = []
    _obj_update_5 = []
    _obj_update_30 = []

    _better_button = []

    _obj_lang_update = []
    _obj_font_size = []

    @property
    def UPDATE_ALL_FRAME(self):
        """à utilisé en argument d' un objet Update_XX pour que ça s'update 60 fois par seconde"""
        return 42

    @property
    def UPDATE_1(self):
        """à utilisé en argument d' un objet Update_XX pour que ça s'update toute les secondes"""
        return -42

    @property
    def UPDATE_5(self):
        """à utilisé en argument d' un objet Update_XX pour que ça s'update toute les 5 secondes"""
        return 46

    @property
    def UPDATE_30(self):
        """à utilisé en argument d' un objet Update_XX pour que ça s'update toute les 30 secondes"""
        return -46

    def register(self, objet):
        """enregistre un object dans l'update manager, """
        if objet.frequence == self.UPDATE_ALL_FRAME:
            self._obj_update_all_frame.append(objet)
        elif objet.frequence == self.UPDATE_1:
            self._obj_update_1.append(objet)
        elif objet.frequence == self.UPDATE_5:
            self._obj_update_5.append(objet)
        elif objet.frequence == self.UPDATE_30:
            self._obj_update_30.append(objet)
        else:
            print("erreur frequence de fait pas partie de UPDATE_MANAGER.UPDATE_XX", objet)
            a = 3 + "&"

    def register_lang(self, object):
        """enregistre un Updatable_Label ou un Updatable_Button dans l'update manager pour update sa traducion a chaque chagement de langues"""
        self._obj_lang_update.append(object)

    def register_font_size(self, object):
        """enregistre un Updatable dans l'update manager pour update sa font size a chaque chagement de taille de police"""
        self._obj_font_size.append(object)

    def register_bter_labbut(self, obj: Better_Button | Better_Label):
        self._better_button.append(obj)

    def update_bter_button(self):
        for obj in self._better_button:
            obj.update_rotation_origin(obj, 0)

    def update_font_size(self):
        """appelle la méthode update_font_size de tout les object préalablement enregistré dans update manager """
        for obj in self._obj_font_size:
            obj.update_font_size()

    def update_all_lang(self):
        """appelle la méthode update_trad de tout les object de _obj_lang_update """
        for obj in self._obj_lang_update:
            obj.update_trad()

    def update_all_all_frame(self):
        """sensé etre appelé toute les frame (60 fois par secondes)  ^^"""
        for obj in self._obj_update_all_frame:
            obj.update()

    def update_all_1(self):
        """sensé etre appelé toute les secondes ^^"""
        for obj in self._obj_update_1:
            obj.update()

    def update_all_5(self):
        """sensé etre appelé toute les 5 seconde ^^"""
        for obj in self._obj_update_5:
            obj.update()

    def update_all_30(self):
        """sensé etre appelé toute les 30 seconde ^^"""
        for obj in self._obj_update_5:
            obj.update()



UPDATE_MANAGER = Update_Manager()


class Update:
    """
    frequence : UPDATE_MANAGER.UPDATE_XX
    fncton : doit etre une fonction sans argument
    default_register : {bool} [True]
    """

    def __init__(self, frequence: int, fncton, default_register: bool = True) -> None:
        self._function = fncton
        self.frequence = frequence
        if default_register:
            UPDATE_MANAGER.register(self)

    @property
    def var_update(self):
        try:
            return self._function()
        except:
            print("le drone n'est pas co ?")
            return ""


class Update_Label(Update, Updatable_Label):
    """fncton : doit etre une fonction sans argument (id_text prend la valeur que fcton return a un untervale de frequence)"""

    def __init__(self, frequence: int, fncton, default_register: bool = True, id_text: str = "", angle: int = 0,
                 **kw) -> None:
        print(frequence)
        Update.__init__(self, frequence, fncton, default_register)
        print("obj d'app ?")
        Updatable_Label.__init__(self, id_text, angle=angle, **kw)

    def update(self):
        self.id_text = self.var_update
        self.update_trad()


class Update_Button(Update, Updatable_Button):
    """fncton : doit etre une fonction sans argument (id_text prend la valeur que fcton return a un untervale de frequence)"""

    def __init__(self, frequence: int, fncton, default_register: bool = True, id_text: str = "", angle: int = 0,
                 **kw) -> None:
        Update.__init__(self, frequence, fncton, default_register)
        Updatable_Button.__init__(self, id_text=id_text, angle=angle, **kw)

    def update(self):
        self.id_text = self.var_update
        self.update_trad()


class Parametre:
    def __init__(self) -> None:
        # -------------- FONT -------------- #
        self.possibles_font_size = {'titre': [20, 25, 30],
                                    "standard": [15, 18.75, 20],
                                    "petit": [15, 18.75, 20]}
        self._current_font_size = 1
        self.manette_is_connected = False

    @property
    def current_font_size(self):
        return self._current_font_size

    @current_font_size.setter
    def current_font_size(self, value):
        """valeurs qui va de 0 a 2 ou 0 est petit, 1 est medium, 2 est large"""
        self._current_font_size = value
        UPDATE_MANAGER.update_font_size()

    def switsh_font_size(self, value):
        if type(value) == int and value in [0, 1, 2]:
            self.current_font_size = value
        elif value == LANGUES.trad("app.parametre.font_size.petit"):
            self.current_font_size = 0

        elif value == LANGUES.trad("app.parametre.font_size.moyen"):
            self.current_font_size = 1

        elif value == LANGUES.trad("app.parametre.font_size.grand"):
            self.current_font_size = 2
        else:
            print(f" value : {value} n'est pas sensé etre value dans le current_font_size, c'est imporsible")
            a = "a" + 1

    def get_curent_font_size(self, font_size_type: str):
        """font_size_type peut etre "titre", "standard" ou "petit """
        return self.possibles_font_size[font_size_type][self.current_font_size]


class all_update_button(Updatable_Button, Update):
    def __init__(self, id_text: str, frequence: int, fncton, default_register: bool = True, **kwargs):
        Updatable_Button.__init__(self, id_text, **kwargs)
        Update.__init__(self, frequence=frequence, fncton=fncton, default_register=default_register)


PARAMETRE = Parametre()





if __name__ == "__main__":
    import sys


    def compare(a, b):
        print(f"Taille de l'objet '{a}' de type {type(a)} :", sys.getsizeof(a), "octets")
        print(f"Taille de l'objet '{b}'de type {type(b)} :", sys.getsizeof(b), "octets")


    entier = 2
    chaine = "English"

    compare(entier, chaine)
