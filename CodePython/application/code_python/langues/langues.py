import json
from kivy.uix.label import Label
from kivy.uix.button import Button

ID_ANGLAIS = 1
ID_FRANCAIS = 2
POSSIBLES_LANGUAGES = ["english", "français"]
DEFAULT_LANGUAGE = ID_ANGLAIS

class Langues() :
    def __init__(self) -> None:
        """
        permet de traduire le texte en plein de langues(2)        
        """
        self._dict_langues = {}
        with open("CodePython/application/code_python/langues/lang.json",'r',encoding='utf-8') as file :
            json_langues_file = json.load(file)
            for i in json_langues_file.keys() :
                self.dict_langues[int(i)] = json_langues_file[i]

        self._current_language = DEFAULT_LANGUAGE
    
    @property
    def current_language(self):
        return self._current_language
    
    @current_language.setter
    def current_language(self, value) :
        """current langage dans l'application"""
        if type(value) == int :
            self._current_language = value
        elif type(value) == str :
            if value == "english" or  value == "anglais" :
                self._current_language = ID_ANGLAIS
            elif value == "frensh" or  value == "français" :
                self._current_language = ID_FRANCAIS
                
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
        return self.dict_langues[self.current_language][id_ecriture]
        

LANGUES = Langues()





# ------------------------------------------------------ Updatable Obj ------------------------------------------------------ #



class Updatable() :
    def __init__(self, id_text:str, **kwargs):
        self.text = LANGUES.trad(id_text)
        self.id_text = id_text    
        
    def update_trad(self) :
        self.text = LANGUES.trad(self.id_text)
    
    def __str__(self) :
        return self.text
    
class Updatable_Label(Label,Updatable) :
    """id_text : id du texte traductible dans le fichier json (le text n'est pas obligé d'etre ajouté)
    """
        
    def __init__(self, id_text:str, **kwargs):
        Label.__init__(self,id_text=id_text, **kwargs)
        Updatable.__init__(self, id_text, **kwargs)
        UPDATE_MANAGER.register_lang(self)


class Updatable_Button(Button,Updatable) :
    """id_text : id du texte traductible dans le fichier json (le text n'est pas obligé d'etre ajouté)
    """
    def __init__(self, id_text:str, **kwargs):
        Button.__init__(self,id_text=id_text , **kwargs)
        Updatable.__init__(self, id_text, **kwargs)
        UPDATE_MANAGER.register_lang(self)
        


class Update_Manager() :
    """permet a update des variable contenue dans des object kivy (notament les labels et les buttons)"""
    obj_update = []
    _obj_lang_update = []

    def register(self, object:Updatable) :
        """enregistre un object dans l'update manager, """
        self.obj_update.append(object)
    
    def register_lang(self, object:Updatable_Button|Updatable_Label) :
        """enregistre un Updatable_Label ou un Updatable_Button dans l'update manager pour update sa traducion a chaque chagement de langues"""
        self._obj_lang_update.append(object)
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