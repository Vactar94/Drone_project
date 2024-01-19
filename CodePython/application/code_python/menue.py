from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle

from code_python.layout_button_menu import creat_layout_button_menu
from code_python.langues.langues import Updatable_Label



class Menue(RelativeLayout):
    def __init__(self,ui_screen,notif:dict={}, **kwargs):
        super().__init__(**kwargs)
        self.ui_screen = ui_screen

        self.size = Window.size
        with self.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=(0,0),size=self.size)
            Color(0/255, 200/255, 255/255)
            RoundedRectangle(pos=(self.size[1]*0.025,self.size[1]*0.025),size=(self.size[0]*0.95,self.size[1]*0.95),radius=[30,30])


        titre_page = Updatable_Label(id_text="app.menue.titre_page",pos_hint={"center_x":0.5,"center_y":0.85},color=(0, 0, 0),font_size_type="titre")
         
        button_classique =  creat_layout_button_menu(name="classique",   ui_screen=ui_screen, size_hint=(0.35, 0.25), pos_hint={"center_x":0.3,"center_y":0.3})
        button_automatique= creat_layout_button_menu(name="automatique", ui_screen=ui_screen, size_hint=(0.35, 0.25), pos_hint={"center_x":0.7,"center_y":0.3})
        button_controles =  creat_layout_button_menu(name="controles",   ui_screen=ui_screen, size_hint=(0.35, 0.25), pos_hint={"center_x":0.3,"center_y":0.7})
        button_parametre =  creat_layout_button_menu(name="parametre",   ui_screen=ui_screen, size_hint=(0.35, 0.25), pos_hint={"center_x":0.7,"center_y":0.7})
        print(button_classique.size)
        print(button_automatique.size)
        print(button_controles.size)
        print(button_parametre.size)


        """
        button_classique = Layout_bouton_menue(name="classique",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(1/25),self.size[1]*(2/9)))
        button_automatique = Layout_bouton_menue(name="automatique",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(1/25),self.size[1]*(5/9)))
        button_controles = Layout_bouton_menue(name="controles",ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(2/9),self.size[1]*(2/9)))
        button_parametre = Layout_bouton_menue(name="parametre", ui_screen=ui_screen,size=(self.size[0]*0.15,self.size[0]*0.15),size_hint=(None,None),pos=(self.size[0]*(2/9),self.size[1]*(5/9)))
        """
        
        #add notifications 
        self.notif = notif


        for k in self.notif.keys() :
            self.add_widget(self.notif[k][0])
            self.add_widget(self.notif[k][1])

        self.add_widget(titre_page)
        self.add_widget(button_classique)
        self.add_widget(button_automatique)
        self.add_widget(button_controles)
        self.add_widget(button_parametre)



