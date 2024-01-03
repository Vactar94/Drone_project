import json
from kivy.uix.label import Label
from kivy.uix.button import Button



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

if __name__ == "__main__" :
    import sys

    def compare(a, b) :
        print(f"Taille de l'entier {a} :", sys.getsizeof(a), "octets")
        print(f"Taille de la chaîne {b} :", sys.getsizeof(b), "octets")
    
    entier = 2
    chaine = "English"

    compare(entier, chaine)
