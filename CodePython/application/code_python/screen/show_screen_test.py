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

        # --------------------- return button --------------------- #
        menue_button = Button(text="", color=(0, 0, 0, 0), size_hint=(None, None), size=(60, 60),
                              pos_hint={"center_x": 0.88, "center_y": 0.915}, background_color=(0, 0, 0, 0))
        menue_button.bind(size=self.update_bg, pos=self.update_bg)
        with menue_button.canvas.before:
            Color(0, 0, 0, 0)
            menue_button.bg_rect = Image(source="image/bouton-retour bg_blanc.png", size=menue_button.size,
                                         pos=menue_button.pos)
        menue_button.bind(on_release=self.go_to_menu)

        self.add_widget(self.control_box)
        self.add_widget(menue_button)

    def on_pre_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_enter(*args)

    def go_to_menu(self, button):
        self.manager.current = "ui"
