from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from code_python.tello import DRONE
from code_python.langues.langues import Updatable_Label, Update_Label, UPDATE_MANAGER
from code_python.screen.screen_sous_menu import Screen_sous_menu
from code_python.Manette import CONTOLLER


class Screen_Info_Drone(Screen_sous_menu):

    def __init__(self, **kw):
        icone = Image(source="image/icone_button_automatique_bg.png")
        super().__init__(id_text_titre="app.info_drone_screen.titre", icone=icone,
                         name_screen_target_return_button="parametre", **kw)

        pos_hint_box_state_drone = {"center_x": 0.5, "center_y": 0.7}  # Position de l'info de battery
        pos_hint_box_state_manette = {"center_x": 0.5, "center_y": 0.75}  # Position de l'info de battery
        pos_hint_box_temph = {"center_x": 0.5, "center_y": 0.55}  # Position de l'info temph
        pos_hint_box_batt = {"center_x": 0.5, "center_y": 0.6}  # Position de l'info de battery

        #  ----------------------- info for temph ----------------------- #
        box_temph = FloatLayout(pos_hint=pos_hint_box_temph)
        titre_temph = Updatable_Label(id_text="app.info_drone_screen.temph.titre",
                                      pos_hint={"center_x": 0.3, "center_y": 0.5}, color=(0, 0, 0, 1))

        def update_var_temph() -> str:
            print("temperature")
            if DRONE.is_connected:
                print("temperature oui")
                return str(DRONE.temph)
            else:
                print("temperature non ")
                return "app.drone.non_conn"

        info_temph = Update_Label(frequence=UPDATE_MANAGER.UPDATE_5, fncton=update_var_temph,
                                  pos_hint={"center_x": 0.7, "center_y": 0.5}, color=(0, 0, 0, 1))

        box_temph.add_widget(titre_temph)
        box_temph.add_widget(info_temph)

        # ----------------------- info for batt ----------------------- #

        box_batt = FloatLayout(pos_hint=pos_hint_box_batt)
        titre_batt = Updatable_Label(id_text="app.info_drone_screen.batt.titre",
                                     pos_hint={"center_x": 0.3, "center_y": 0.5}, color=(0, 0, 0, 1))

        def update_var_batt() -> str:
            if DRONE.is_connected:
                print("batterie oui")
                return str(DRONE.battery)
            else:
                print("batterie non ")
                return ""

        info_batt = Update_Label(frequence=UPDATE_MANAGER.UPDATE_5, fncton=update_var_batt,
                                 pos_hint={"center_x": 0.7, "center_y": 0.5}, color=(0, 0, 0, 1))

        box_batt.add_widget(titre_batt)
        box_batt.add_widget(info_batt)

        # ----------------------- info for state_drone ----------------------- #

        box_state_drone = FloatLayout(pos_hint=pos_hint_box_state_drone)
        titre_state_drone = Updatable_Label(id_text="app.info_drone_screen.state_drone.titre",
                                     pos_hint={"center_x": 0.3, "center_y": 0.5}, color=(0, 0, 0, 1))

        def update_var_state_drone() -> str:
            if DRONE.is_connected:
                return "app.info_drone_screen.state_drone.text.true"
            else:
                return "app.info_drone_screen.state_drone.text.false"

        info_state_drone = Update_Label(frequence=UPDATE_MANAGER.UPDATE_5, fncton=update_var_state_drone,
                                 pos_hint={"center_x": 0.7, "center_y": 0.5}, color=(0, 0, 0, 1))

        box_state_drone.add_widget(titre_state_drone)
        box_state_drone.add_widget(info_state_drone)

        # ----------------------- info for state_manette ----------------------- #

        box_state_manette = FloatLayout(pos_hint=pos_hint_box_state_manette)
        titre_state_manette = Updatable_Label(id_text="app.info_drone_screen.state_manette.titre",
                                      pos_hint={"center_x": 0.3, "center_y": 0.5}, color=(0, 0, 0, 1))

        def update_var_state_manette() -> str:
            if CONTOLLER.is_connected:
                return "app.info_drone_screen.state_manette.text.true"
            else:
                return "app.info_drone_screen.state_manette.text.false"

        info_state_manette = Update_Label(frequence=UPDATE_MANAGER.UPDATE_5, fncton=update_var_state_manette,
                                  pos_hint={"center_x": 0.7, "center_y": 0.5}, color=(0, 0, 0, 1))

        box_state_manette.add_widget(titre_state_manette)
        box_state_manette.add_widget(info_state_manette)

        # ----------------------- general ----------------------- #

        self.add_widget(box_state_drone)
        self.add_widget(box_state_manette)
        self.add_widget(box_temph)
        self.add_widget(box_batt)
