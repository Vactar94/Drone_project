from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Rectangle, Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen



class Rectangle_hint(Widget):
    """Widget coloré en la couleur passé dans color (par défaut blanc)
    color : Couleur (RGBA)=(0, 0, 0, 0)"""

    def __init__(self, color:tuple=(1, 1, 1, 1),  **kwargs):
        super().__init__(**kwargs)
        # Création d'un rectangle rouge avec size_hint et pos_hint
        with self.canvas:
            Color(*color)  # Couleur (RGBA)
            self.rrect = RoundedRectangle(pos=self.pos, size=self.size)
            
        self.bind(pos=self.update_rrect_pos_size, size=self.update_rrect_pos_size)

    def update_rrect_pos_size(self, instance, value):
        # Mettez à jour la position et la taille du RoundedRectangle en fonction du widget parent
        self.rrect.pos = self.pos
        self.rrect.size = self.size


class RoundedRectangle_hint(Widget):
    def __init__(self, color=(1, 1, 1, 1), radius=[0, 0], **kwargs):
        super().__init__(**kwargs)

        # Créez le RoundedRectangle initial
        with self.canvas:
            Color(*color)
            self.rrect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)

        # Liez la mise à jour du RoundedRectangle aux changements de pos et size du widget parent
        self.bind(pos=self.update_rrect_pos_size, size=self.update_rrect_pos_size)

    def update_rrect_pos_size(self, instance, value):
        # Mettez à jour la position et la taille du RoundedRectangle en fonction du widget parent
        self.rrect.pos = self.pos
        self.rrect.size = self.size




class Better_Button(Button):
    _get_added_widget = []
    def __init__(self, angle:int=0, **kwargs):
        super().__init__(**kwargs)

        # Ajoutez une transformation pour inverser le texte verticalement
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=angle, origin=self.center)

        with self.canvas.after:
            PopMatrix()

        self.rot.origin = self.center

    def on_size(self, instance, value):
        # Mettez à jour l'origine de la rotation lorsque la taille change
        self.rot.origin = self.center
        



    @property
    def get_added_widget(self)-> list :
        return self._get_added_widget

    #def update_size_pos_button(self ,button) :
        
    
    def add_widget(self, widget, index=0, canvas=None):
        self.get_added_widget.append(widget)
        return super().add_widget(widget, index, canvas)

class Better_Label(Label):
    def __init__(self, angle:int=0, **kwargs):
        super().__init__(**kwargs)

        # Ajoutez une transformation pour inverser le texte verticalement
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=angle, origin=self.center)

        with self.canvas.after:
            PopMatrix()

    def on_size(self, instance, value):
        # Mettez à jour l'origine de la rotation lorsque la taille change
        self.rot.origin = self.center


class Better_Screen(Screen) :
    _get_added_widget = []
    
    def __init__(self,notifications : dict = None, **kw):
        
        super().__init__(**kw)
        self.streamable = False


        if notifications != None and type(notifications) != dict:
            print("notification incorrecte il faut passer un dictonnaire enculer ")
            print(notifications.text)
            a = 1+"g"
        else :
            self.notifications = notifications

    @property
    def get_added_widget(self)-> list :
        return self._get_added_widget
    
    def add_widget(self, widget, index=0, canvas=None):
        self.get_added_widget.append(widget)
        return super().add_widget(widget, index, canvas)
    



    def update_bg(self,element,value):
        """update les positions des bg de pleins de trucs"""
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size
    
    def on_pre_enter(self,*args) :
        return super().on_pre_enter(*args)

    def on_pre_leave(self, *args):
        return super().on_pre_leave(*args)
    
    def __str__(self) :
        return self.name

class RoundedImage(Widget):
    def __init__(self, image_source:str, radius:list[int,int], **kwargs):
        self.image = Image(source=image_source, allow_stretch=True, keep_ratio=False)
        super(RoundedImage, self).__init__(**kwargs)
        
        self.add_widget(self.image)

        self.radius = radius

    def on_size(self, instance, value):
        self.image.size = self.size
        self.image.pos = self.pos

    def on_pos(self, instance, value):
        self.image.pos = value