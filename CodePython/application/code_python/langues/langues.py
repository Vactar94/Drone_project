import json
from dataclasses import dataclass
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner



class Langues() :
    POSSIBLES_LANGUAGES = []

    def __init__(self) -> None:
        """
        permet de traduire le texte en plein de langues(2)        
        """
        self._dict_langues = {}
        with open("CodePython/application/code_python/langues/lang.json",'r',encoding='utf-8') as file :
            json_langues_file = json.load(file)
            for i in json_langues_file.keys() :
                self.POSSIBLES_LANGUAGES.append(i)

                self.dict_langues[i] = json_langues_file[i]
        
        self._current_language = list(json_langues_file.keys())[0]
    
    @property
    def current_language(self):
        return self._current_language
    
    @current_language.setter
    def current_language(self, value) :
        """current langage dans l'application"""
        if type(value) == int :
            self._current_language = list(self.dict_langues.keys())[value]
        elif value in self.dict_langues.keys() :
            self._current_language = value
        else :
            print(f"value : {value} qui est entré dans le setter de current_language n'est pas comforme")
            a = 1 +"a"

        UPDATE_MANAGER.update_all_lang()



    @property
    def dict_langues(self):
        return self._dict_langues
    
    @dict_langues.setter
    def dict_langues(self, value) :
        """{id_Langue:{id_écriture:str}}"""
        self._dict_langues = value
    
    def trad(self,id_ecriture) -> str :
        """transphorme un id_ecriture en str"""
        try :
            if self.dict_langues[self.current_language][id_ecriture] == "" :
                return id_ecriture
            else  : 
                return self.dict_langues[self.current_language][id_ecriture] 
        except :
            return id_ecriture

    def contre_trad(self,text)-> str|list :
        """transphorme un id_ecriture en str si il exsite, sinon fait une erreur"""
        id_text = []
    
        for key in self.dict_langues[self.current_language].keys() :
            if self.dict_langues[self.current_language][key] == text :
                id_text.append(key)
    
        if len(id_text) == 0 :
            return text
        elif len(id_text) == 1 :
            return id_text[0] 
        else :
            return id_text


LANGUES = Langues()


# ------------------------------------------------------ Updatable Obj ------------------------------------------------------ #


class Updatable_font():

    def __init__(self, font_size_type:str) -> None:
        self.font_size_type = font_size_type
        self.update_font_size()
        UPDATE_MANAGER.register_font_size(self)

        
    def update_font_size(self) :
        print(self)
        print(self.font_size_type)
        self.font_size = PARAMETRE.get_curent_font_size(self.font_size_type)
        print(self.font_size)
        print()


class Updatable_lang() :
    def __init__(self, id_text:str) -> None:
        self.id_text = id_text

        self.update_trad()
        UPDATE_MANAGER.register_lang(self)
    
    def update_trad(self) :
        self.text = LANGUES.trad(self.id_text)


class Updatable(Updatable_font,Updatable_lang) :
    def __init__(self, id_text:str, font_size_type:str="standard", **kwargs):
        Updatable_font.__init__(self,font_size_type=font_size_type)
        Updatable_lang.__init__(self, id_text)

    def __str__(self) :
        return self.text




class Updatable_Spinner(Updatable_font, Spinner):
    """version Updatabe de kivy.uix.Spinner
    id_values : list des id du text des values {str}
    id text : id du text {str}
    Uptate_values:bool=True
    Uptate_text:bool=True
    """

    def __init__(self, id_values:list=[],  id_text:str="", Uptate_values:bool=True, Uptate_text:bool=True, font_size_type="standard", **kwargs):
        # Appeler le constructeur de la classe mère Updatable_font
        Updatable_font.__init__(self, font_size_type)
        # Appeler le constructeur de la classe mère Spinner
        Spinner.__init__(self, **kwargs)

        self.Uptate_values = Uptate_values
        self.Uptate_text = Uptate_text

        self.id_values = id_values
        self.id_text = id_text
        self.values = id_values
        self.update_trad()

        
           
        
    def update_trad(self) :
        """update les values"""
        if self.Uptate_values :
            for i in range(len(self.values)) :
                self.values[i] = LANGUES.trad(self.id_values[i])
        if self.Uptate_text :
            self.text = LANGUES.trad(self.id_text)
    
    def __str__(self) :
        return f"spinner : {self.values}"

    
class Updatable_Label(Label,Updatable) :
    """id_text : id du texte traductible dans le fichier json (le text n'est pas obligé d'etre ajouté) {str}
    """
        
    def __init__(self, id_text:str, **kwargs):
        Label.__init__(self,id_text=id_text, **kwargs)
        Updatable.__init__(self, id_text, **kwargs)



class Updatable_Button(Button,Updatable) :
    """id_text : id du texte traductible dans le fichier json (le text n'est pas obligé d'etre ajouté) {str}
    """
    def __init__(self, id_text:str, **kwargs):
        Button.__init__(self,id_text=id_text , **kwargs)
        Updatable.__init__(self, id_text, **kwargs)

        


class Update_Manager() :
    """permet a update des variable contenue dans des object kivy (notament les labels et les buttons)"""
    _obj_update = []
    _obj_lang_update = []
    _obj_font_size = []

    def register(self, object:Updatable) :
        """enregistre un object dans l'update manager, """
        self._obj_update.append(object)
    
    def register_lang(self, object:Updatable_Button|Updatable_Label|Updatable_Spinner) :
        """enregistre un Updatable_Label ou un Updatable_Button dans l'update manager pour update sa traducion a chaque chagement de langues"""
        self._obj_lang_update.append(object)
    
    def register_font_size(self,  object:Updatable_Button|Updatable_Label|Updatable_Spinner) :
        """enregistre un Updatable dans l'update manager pour update sa font size a chaque chagement de taille de police"""

        self._obj_font_size.append(object)


    
    def update_font_size(self) :
        """appelle la méthode update_font_size de tout les object préalablement enregistré dans update manager """
        print("update_font_size")
        for obj in self._obj_font_size :
            obj.update_font_size()




    def update_all_60(self) :
        """c'est la et ça servira quand ça servira"""
        pass

    def update_all_1(self) :
        """c'est la et ça servira quand ça servira"""
        pass


    def update_all_lang(self) :
        """appelle la méthode update_trad de tout les object de _obj_lang_update """
        for obj in self._obj_lang_update :
            obj.update_trad()




UPDATE_MANAGER = Update_Manager()




class Parametre :
    def __init__(self) -> None:
        # -------------- FONT -------------- #
        self.possibles_font_size = {'titre':[20, 25, 30],
                                    "standard":[15, 18.75, 20],
                                    "petit":[15, 18.75, 20]}
        self._current_font_size = 1
    
    @property
    def current_font_size(self) :
        print(self._current_font_size)
        return self._current_font_size

    @current_font_size.setter 
    def current_font_size(self, value) :
        """valeurs qui va de 0 a 2 ou 0 est petit, 1 est medium, 2 est large"""
        self._current_font_size = value
        print("current_font_size.setter")
        UPDATE_MANAGER.update_font_size()
 
        
    
    def switsh_font_size(self, value) :
        if type(value) == int and value in [0, 1, 2]:
            self.current_font_size = value
        elif value == LANGUES.trad("app.parametre.font_size.petit") :
            print("Petit")
            self.current_font_size = 0
        elif value == LANGUES.trad("app.parametre.font_size.moyen") :
            print("moyen")
            self.current_font_size = 1
        elif value == LANGUES.trad("app.parametre.font_size.grand") :
            print("Grand")
            self.current_font_size = 2
        else :
            print(f" value : {value} n'est pas sensé etre value dans le current_font_size, c'est imporsible")
            a = "a"+1

    def get_curent_font_size(self, font_size_type:str) :
        """font_size_type peut etre "titre", "standard" ou "petit """
        return self.possibles_font_size[font_size_type][self.current_font_size]

            
        
        

PARAMETRE = Parametre()


if __name__ == "__main__" :
    import sys

    def compare(a, b) :
        print(f"Taille de l'entier '{a}' :", sys.getsizeof(PARAMETRE), "octets")
        print(f"Taille de la chaîne '{b}' :", sys.getsizeof(b), "octets")
    
    entier = 2
    chaine = "English"

    compare(entier, chaine)
