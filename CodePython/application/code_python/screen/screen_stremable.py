import time
from threading import Thread

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

        self.image_streem = Image(size_hint=[1, 1], pos_hint={"y": 0.1})

        self.box_streem = BoxLayout(size_hint=(None, None), size=self.size)

        self.control_box = ControlBox(pos_hint={"center_x": 0.5, "center_y": 0.5})

        # self.box_streem.add_widget(self.image_streem)

        # --- menu button --- #

        menu_button = Button(text="", color=(0, 0, 0, 0), size_hint=(None, None), size=(60, 60),
                             pos_hint={"center_x": 0.88, "center_y": 0.915}, background_color=(0, 0, 0, 0))
        menu_button.bind(size=self.update_bg, pos=self.update_bg)
        with menu_button.canvas.before:
            Color(0, 0, 0, 0)
            menu_button.bg_rect = Image(source="image/bouton-retour bg_blanc.png", size=menu_button.size,
                                        pos=menu_button.pos)
        menu_button.bind(on_release=self.go_to_menu)

        self.add_widget(menu_button)
        self.add_widget(self.box_streem)
        self.add_widget(self.control_box)

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
            self.go_to_menu("ui")
            NOTIF_MANAGER.Waiting_notifications["D"][0] = True
        else:
            NOTIF_MANAGER.Waiting_notifications["D"][1] = True

    def on_pre_leave(self, *args):

        if DRONE.is_connected:
            DRONE.stop_streeming()
        return super().on_pre_leave(*args)

    def go_to_menu(self, value):
        self.manager.current = "ui"

    def update_opacity(self, opacity: bool):
        self.control_box.opacity_layout = opacity

    def get_events(self):
        return self.control_box.get_events()


class ControlBox(FloatLayout):
    _drone_is_flying = False

    def __init__(self, **kw):
        super().__init__(**kw)
        self._opacity = 1

        # --- joystick --- #
        self._joy_r = Joystick(size_hint=(1.0 / 2.5, 1.0 / 2.5), pos_hint={"center_x": 0.25, "center_y": 0.8},
                               inner_background_color=(100 / 255, 50 / 255, 50 / 255, 0.2),
                               pad_background_color=(220 / 255, 120 / 255, 120 / 255, 0.6),
                               outer_background_color=(150 / 255, 40 / 255, 40 / 255, 0.1))
        self._joy_l = Joystick(size_hint=(1.0 / 2.5, 1.0 / 2.5), pos_hint={"center_x": 0.25, "center_y": 0.2},
                               inner_background_color=(50 / 255, 50 / 255, 100 / 255, 0.2),
                               pad_background_color=(120 / 255, 120 / 255, 220 / 255, 0.6),
                               outer_background_color=(40 / 255, 40 / 255, 150 / 255, 0.1))

        # --- land button --- #

        def land_button_text() -> str:
            if self._drone_is_flying:
                return "app.drone.control.land_button.air"
            else:
                return "app.drone.control.land_button.sol"

        self.land_button = Update_Button(id_text="app.drone.control.land_button.sol", fncton=land_button_text,
                                         frequence=UPDATE_MANAGER.UPDATE_ALL_FRAME,
                                         pos_hint={"center_x": 0.7, "center_y": 0.15}, background_color=(1, 0, 1, 0.5),
                                         size_hint=(0.2, 0.1), angle=-90)
        self.land_button.bind(on_release=self.decolage_atterrissage)

        self.add_widget(self.land_button)
        self.add_widget(self._joy_r)
        self.add_widget(self._joy_l)

        self.opacity_layout = True
        UPDATE_MANAGER.register_controller(self)

        self.opacity_layout = True

    def get_events(self):
        lr, fb, ud, yv = 0, 0, 0, 0
        speed = 50
        if 1 >= self._joy_l.magnitude >= 0 and 1 >= self._joy_r.magnitude >= 0:
            # AXE X
            if 225 > self._joy_l.radians > 135:  # droite
                lr = -int(self._joy_l.magnitude * speed)
            elif self._joy_l.radians > 315 or self._joy_l.radians < 45:  # gauche
                lr = int(self._joy_l.magnitude * speed)
            # AXE Y
            elif 45 < self._joy_l.radians < 135:  # front
                fb = -int(self._joy_l.magnitude * speed)
            elif 225 < self._joy_l.radians < 315:  # back
                fb = int(self._joy_l.magnitude * speed)

            # UP Down
            if 225 > self._joy_r.radians > 135:
                ud = -int(self._joy_r.magnitude * speed)
            elif self._joy_r.radians > 315 or self._joy_r.radians < 45:
                ud = int(self._joy_r.magnitude * speed)
            # rotation vertical axe
            elif 45 < self._joy_r.radians < 135:
                yv = -int(self._joy_r.magnitude * speed)
            elif 225 < self._joy_r.radians < 315:
                yv = int(self._joy_r.magnitude * speed)
            print([fb, lr, ud, yv])
            return [fb, lr, ud, yv]
        else:
            print([0, 0, 0, 0])
            return [0, 0, 0, 0]

    def decolage_atterrissage(self, button: Button):
        Thread(target=self.button_update, args=[button]).start()

        if DRONE.is_connected:

            if self._drone_is_flying:
                print("land")
                DRONE.drone.land()

                self.a = False
            else:
                print("takeoff")
                print(DRONE.drone.is_flying)
                DRONE.drone.takeoff()
                self._drone_is_flying = True

        time.sleep(1)
        button.disabled = False

    def button_update(self, button):

        button.disabled = True
        time.sleep(2)
        button.disabled = False

    def update_bg(self, element, value):
        """update les positions des bg de pleins de trucs"""
        element.bg_rect.pos = element.pos
        element.bg_rect.size = element.size

    def go_to_menu(self, button):
        self.parent.go_to_menu(button)

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
            widget.opacity = self._opacity

    def update_controller(self, value):
        self.opacity_layout = not value
