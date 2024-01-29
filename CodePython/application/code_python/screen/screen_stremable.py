from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from code_python.tello import DRONE
from code_python.notification import NOTIF_MANAGER
from code_python.better_Kivy import Better_Screen
from code_python.global_function import is_wifi_drones_connected
from code_python.langues.langues import Update_Button, UPDATE_MANAGER
from code_python.joystick import Joystick


class Screen_Stramable(Better_Screen):

    def __init__(self, notifications: dict = None, **kw):
        super().__init__(notifications, **kw)
        self.streamable = True

        self.size = Window.size

        self.image_streem = Image(size=self.size)
        self.box_streem = BoxLayout(size_hint=(None, None), size=self.size)

        self.control_box = ControlBox(pos_hint={"center_x": 0.5, "center_y": 0.5})

        menue_button = Button(text="", color=(0, 0, 0), size_hint=(None, None), size=(60, 60),
                              pos_hint={"center_x": 1 - 0.87, "center_y": 0.9}, background_color=(0, 0, 0, 0))
        with menue_button.canvas.before:
            Color(0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg.png", size=menue_button.size,
                                         pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menue, size=self.update_bg, pos=self.update_bg)

        self.box_streem.add_widget(self.image_streem)
        self.add_widget(self.box_streem)
        self.add_widget(self.control_box)
        self.add_widget(menue_button)

    def on_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_enter(*args)

    def on_pre_enter(self):
        """check que le drone est connecté, oui-> le streem commence puis notif l'app que le drone est co
                                            non -> notif l'app que le drone n'est pas co
        """
        self.control_box.land_button.update_rotation_origin(0, 0)
        if is_wifi_drones_connected() and not DRONE.is_connected:
            DRONE.connect()
        a = DRONE.start_streeming()
        print(f"le streem a commencé : {a}")
        if not a:
            self.go_to_menue("ui")
            NOTIF_MANAGER.Waiting_notifications["D"][0] = True
        else:
            NOTIF_MANAGER.Waiting_notifications["D"][1] = True

    def on_pre_leave(self, *args):

        if DRONE.is_connected:
            DRONE.stop_streeming()
        return super().on_pre_leave(*args)

    def go_to_menue(self, value):
        self.manager.current = "ui"

    def update_opacity(self, opacity: bool):
        self.control_box.opacity_layout = opacity


class ControlBox(FloatLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._opacity = 1

        joy_r = Joystick(size_hint=(1.0 / 2.5, 1.0 / 2.5), pos_hint={"center_x": 0.25, "center_y": 0.8},
                         inner_background_color=(100 / 255, 50 / 255, 50 / 255, 0.2),
                         pad_background_color=(220 / 255, 120 / 255, 120 / 255, 0.6),
                         outer_background_color=(150 / 255, 40 / 255, 40 / 255, 0.1))
        joy_l = Joystick(size_hint=(1.0 / 2.5, 1.0 / 2.5), pos_hint={"center_x": 0.25, "center_y": 0.2},
                         inner_background_color=(50 / 255, 50 / 255, 100 / 255, 0.2),
                         pad_background_color=(120 / 255, 120 / 255, 220 / 255, 0.6),
                         outer_background_color=(40 / 255, 40 / 255, 150 / 255, 0.1))

        # --- land button --- #

        def land_button_text() -> str:
            if DRONE.is_flying:
                return "app.drone.control.land_button.air"
            else:
                return "app.drone.control.land_button.sol"

        self.land_button = Update_Button(id_text="app.drone.control.land_button.sol", fncton=land_button_text,
                                         frequence=UPDATE_MANAGER.UPDATE_ALL_FRAME,
                                         pos_hint={"center_x": 0.7, "center_y": 0.15}, background_color=(1, 0, 1, 0.5),
                                         size_hint=(0.2, 0.1), angle=-90)
        self.land_button.bind(on_release=self.switsh_opacity)

        self.add_widget(self.land_button)
        self.add_widget(joy_r)
        self.add_widget(joy_l)

        self.opacity_layout = True

    @property
    def opacity_layout(self):
        if self._opacity == 1:
            return True
        elif self._opacity == 0:
            return False
        else:
            self._opacity = 0
            return False

    @opacity_layout.setter
    def opacity_layout(self, value):
        if value:
            self._opacity = 1
        else:
            self._opacity = 0
        for widget in self.children:
            print(widget.opacity)
            widget.opacity = self._opacity

    def switsh_opacity(self, button):
        self.opacity_layout = not self.opacity_layout
