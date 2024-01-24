import time

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

from code_python.langues.langues import Updatable_Label
from code_python.better_Kivy import RoundedRectangle_hint, Rectangle_hint


class AnimationHint:
    def __init__(self, widget, duration):
        self.widget = widget
        self.duration = duration
        print(type(self.widget.parent))
        print(type(self.widget))

    def start(self):
        print(type(self.widget.parent), self.widget.parent.width, self.widget.parent.height)
        print(type(self.widget), self.widget.width, self.widget.height, self.widget.pos)
        self.animation = Animation(x=int(self.widget.parent.width // 2), duration=self.duration, transition="out_quint")
        self.animation.bind(on_complete=self.anim1_completed)

        self.animation2 = Animation(x=self.widget.parent.width, duration=self.duration, transition="in_quint")
        self.animation2.bind(on_complete=self.anim2_completed)
        self.animation.start(self.widget)

    def anim1_completed(self, layout, value):
        print("anim1_completed")
        print(type(self.widget.parent), self.widget.parent.width, self.widget.parent.height)
        print(type(self.widget), self.widget.width, self.widget.height, self.widget.pos)
        self.animation2.start(self.widget)

    def anim2_completed(self, layout, value):
        print("anim2_completed")
        print(type(self.widget.parent), self.widget.parent.width, self.widget.parent.height)
        print(type(self.widget), self.widget.width, self.widget.height, self.widget.pos)
        self.widget.pos[0] = - self.widget.parent.width

    def stop(self):
        if self.animation:
            self.animation.stop(self.widget)
        elif self.animation2:
            self.animation2.stop(self.widget)


class Notification(FloatLayout):

    def __init__(self, text, duration: int = 2, **kwargs) -> None:
        self.name = text
        super().__init__(size_hint=(0.7, 0.1), pos=(0, 0), **kwargs)
        print(self.pos, "Notif")

        self.neutral_x_hint = -1

        self.bg_rect = RoundedRectangle_hint(color=(1, 1, 1, 1),
                                             size_hint=(1, 1),
                                             pos_hint={"x": 0, "y": 0},
                                             radius=[10, 10])
        self.bg_rect_ombre = RoundedRectangle_hint(color=(0, 0, 0, 0.3),
                                                   size_hint=(1, 1),
                                                   pos_hint={"x": -0.14, "y": -0.2},
                                                   radius=[10, 10])

        text = Updatable_Label(id_text=text, color=(0, 0, 0), pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.anim = AnimationHint(self, duration)

        self.add_widget(self.bg_rect_ombre)
        self.add_widget(self.bg_rect)
        self.add_widget(text)

    def __str__(self) -> str:
        return "Notification : " + self.name

    def update_bg(self, element, value):
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size

        element.bg_rect_ombre.pos = [element.pos[0] - element.size[0] // 15, element.pos[1] - element.size[1] // 15]
        element.bg_rect_ombre.size = element.size

    def start_anim(self):
        print(self)
        self.anim.start()


def crea_notif(duration: int = 1) -> dict[str:list[Notification]]:
    """
            crée un dictonnaire avec avec le type de information en clefs et en valeurs une une list avec en 0 que l'inforamtion est vrai et l'autre que l'information est fausse
            layout[layout_max, curent_layout]
        """
    dict_notif = {}
    dict_notif["M"] = [Notification("app.notif.manette_non_connecte", duration=duration),
                       Notification("app.notif.manette_connecte", duration=duration)]
    dict_notif["D"] = [Notification("app.notif.drone_non_connecte", duration=duration),
                       Notification("app.notif.drone_connecte", duration=duration)]

    return dict_notif


class Notif_Manager:
    _Waiting_notifications = {"M": {0: 0, 1: 0}, "D": {0: 0,
                                                       1: 0}}  # ici on créé un dirctionnaire avec en clefs le nom de la notif, et en valuers un dirctionnaire avec en celfs la valeurs de la notif et en valeurs si il faut envoyer la notif ou pas dans la prochiane frame (True or False)

    @property
    def Waiting_notifications(self):
        """{"lettre de la notif":{0(non):value(True/False), 1(oui):value(True/False)}}"""
        return self._Waiting_notifications

    def put_notification(self, screen: Screen = None, waiting_frames: int = 0):
        pass


NOTIF_MANAGER = Notif_Manager()

if __name__ == "__main__":
    class test_app(App):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def build(self):
            notif_box = Notification("app.notif.manette_non_connecte")
            app_box = n_Box_layout(size=Window.size)
            app_box.add_widget(notif_box)

            button = Button(text='Cliquez-moi !', size_hint=(None, None))
            button.bind(on_press=lambda instance: notif_box.start_anim())
            app_box.add_widget(button)

            return app_box


    class n_Box_layout(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas.before:
                Color(1, 0, 0.96)
                Rectangle(size=self.size)


    test_app().run()
