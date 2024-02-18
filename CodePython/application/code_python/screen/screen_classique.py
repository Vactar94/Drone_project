from code_python.screen.screen_stremable import Screen_Stramable

from code_python.screen.screen_stremable import ControlBox


class Screen_Classique(Screen_Stramable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_enter(*args)

    def go_to_menu(self, button):
        self.manager.current = "ui"

