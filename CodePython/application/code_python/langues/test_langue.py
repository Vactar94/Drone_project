from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class Updatable:
    def __init__(self, id_text:str=None, **kwargs):
        self.id_text = id_text

    def update(self):
        self.text = 


class U_Label(Label,Updatable) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class U_Button(Button,Updatable) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class test_app(App) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.var = "Cliquez-moi"
        
    def build(self) :

        app_box = BoxLayout()

        button = Button(text='Cliquez-moi',size_hint=(None, None))
        button.bind(on_press=self.modifi_var)

        self.label = U_Label(text=self.var, updating_variable=self.var,pos_hint={'center_x': 0.5, 'center_y': 0.5})
        app_box.add_widget(button)
        app_box.add_widget(self.label)
        
        return app_box
        
    def modifi_var(self,button) :
        self.var += "|"
        self.label.update()


if __name__ == "__main__" :
    test_app().run()