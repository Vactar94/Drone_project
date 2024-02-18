from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color


from code_python.better_Kivy import Better_Screen
from code_python.screen.screen_stremable import ControlBox


class Test_Screen(Better_Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        # --------------------- control_box --------------------- #
        self.control_box = ControlBox(pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.control_box)

    def get_events(self):
        return self.control_box.get_events()

    def on_pre_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_enter(*args)

    def go_to_menu(self, button):
        self.manager.current = "ui"


