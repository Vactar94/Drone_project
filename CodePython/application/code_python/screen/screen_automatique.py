from code_python.screen.screen_stremable import Screen_Stramable, ControlBox

class Screen_Automatique(Screen_Stramable):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # --------------------- control_box --------------------- #
        self.control_box = ControlBox(pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.control_box)

    def on_pre_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        self.control_box.land_button.update_rotation_origin(0, 0)
        return super().on_enter(*args)

    def go_to_menu(self, button):
        self.manager.current = "ui"