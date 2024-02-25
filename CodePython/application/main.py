from threading import Thread

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.screenmanager import ScreenManager, RiseInTransition
from kivy.config import Config
from kivy.clock import Clock

from code_python.notification import crea_notif
from code_python.better_Kivy import Better_Screen
from code_python.screen.menue import Menue
from code_python.screen.accueil import Accueil
from code_python.global_function import SYSTEM, is_wifi_drones_connected
from code_python.tello import DRONE
from code_python.notification import NOTIF_MANAGER
from code_python.langues.langues import UPDATE_MANAGER
# -- les screens -- #
from code_python.screen.screen_automatique import Screen_Automatique
from code_python.screen.screen_info_drone import Screen_Info_Drone
from code_python.screen.show_screen_test import Test_Screen
from code_python.screen.screen_classique import Screen_Classique
from code_python.screen.screen_controles import Screen_Controles
from code_python.screen.screen_parametre import Screen_Parametre

Window.size = [360, 720]

# Window.size = [1000, 620]
Window.OS = SYSTEM


def update_drone_connection(application):
    application.dm.is_connected = is_wifi_drones_connected()


class The_app(App):
    """
    la main_app a partir du quel l'app se lance
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager(transition=RiseInTransition())
        self.dm = DRONE
        self.seconde = 0
        self.screens = []

    def build(self):
        # création des screens

        notifs = crea_notif()

        ui_screen = UiScreen(name='ui', notifications=notifs.copy())
        controle_screen = Screen_Controles(name='controles', notifications=notifs.copy())
        parametre_screen = Screen_Parametre(name="parametre", notifications=notifs.copy())
        classique_screen = Screen_Classique(name="classique", notifications=notifs.copy())
        automatique_screen = Screen_Automatique(name="automatique", notifications=notifs.copy())
        screen_info_drone = Screen_Info_Drone(name="info_drone", notifications=notifs.copy())

        test_screen = Test_Screen(name="test", notifications=notifs.copy())

        self.screens.append(ui_screen)
        self.screens.append(controle_screen)
        self.screens.append(parametre_screen)
        self.screens.append(classique_screen)
        self.screens.append(automatique_screen)
        self.screens.append(screen_info_drone)

        self.screens.append(test_screen)

        # ajout des screens au screen manager

        self.sm.add_widget(ui_screen)
        self.sm.add_widget(classique_screen)
        self.sm.add_widget(controle_screen)
        self.sm.add_widget(automatique_screen)
        self.sm.add_widget(parametre_screen)
        self.sm.add_widget(screen_info_drone)

        self.sm.add_widget(test_screen)

        Clock.schedule_interval(self.update_60_fps, 1.0 / 60.0)
        Clock.schedule_interval(self.update_30_fps, 1.0 / 30.0)
        Clock.schedule_interval(self.update_1_seconde, 1.0 / 1.0)
        Clock.schedule_interval(self.update_5_seconde, 5.0)
        Clock.schedule_interval(self.update_30_seconde, 30.0)

        for screen in self.screens:
            if not screen.streamable:
                for notifs in screen.notifications.values():
                    for notif in notifs:
                        notif.init_after()

        return self.sm

    def update_30_seconde(self, dt):
        UPDATE_MANAGER.update_all_30()

    def update_5_seconde(self, dt):
        UPDATE_MANAGER.update_all_5()
        Thread(target=update_drone_connection, args=[self]).start()



    def update_1_seconde(self, dt):
        self.seconde += 1
        UPDATE_MANAGER.update_all_1()

    def update_30_fps(self, dt):
        self.update_streem()

    def update_60_fps(self, dt):
        """main_loop avec toutes les updates"""
        self.update_notif()
        UPDATE_MANAGER.update_all_all_frame()

    def update_streem(self):
        """update les images 30 fois par seconde et l'affiche sur le self.curent_screen.background qui est une image stocké dans box_background"""
        screen = self.sm.current_screen
        if screen.streamable:
            print(screen.image_streem.x, "screen.image_streem.x")
            print(screen.image_streem.y, "screen.image_streem.y ")
            if self.dm.is_connected:
                screen.image_streem = self.dm.get_image(screen.image_streem)
                moove = screen.get_events()
                self.dm.main_loop(moove)
            else:
                self.connect_drone()


    def update_notif(self):
        """prend tout NOTIF_MANAGER.Waiting_notifications et les affiches sur le sm.curent_screen"""
        W_N = NOTIF_MANAGER.Waiting_notifications
        for k in W_N.keys():
            for i in W_N[k].keys():
                if W_N[k][i]:
                    self.sm.current_screen.notifications[k][i].start_anim()
                    W_N[k][i] = False

    def connect_drone(self) -> bool:
        if is_wifi_drones_connected():
            return self.dm.connect()
        return False


class UiScreen(Better_Screen):
    """setup un peu cocase pour avoir un kv.uix.screen et kv.uix.pagelayout"""

    def __init__(self, **kwargs):

        super(UiScreen, self).__init__(**kwargs)

        pages = UI(ui_screen=self)

        self.add_widget(pages)
        # adding notif
        for list_value in self.notifications.values():
            for notif in list_value:
                self.add_widget(notif)

    """  """

    def go_to(self, value, name_of_the_target_screen: str):
        self.manager.current = name_of_the_target_screen


# -- les mains pages de l'app -- #
class UI(PageLayout):
    def __init__(self, ui_screen, **kwargs):
        self.ui_screen = ui_screen  # Stocker une référence à UiScreen
        super(UI, self).__init__(**kwargs)

        self.page1 = Accueil(ui_screen=ui_screen)
        self.page2 = Menue(ui_screen=ui_screen)

        self.add_widget(self.page1)
        self.add_widget(self.page2)

    def go_to_menue(self, value):
        self.manager.current = "ui"


if __name__ == "__main__":
    Config.set('kivy', 'window_icon', 'CodePython/application/image/logo_drone_aid.ico')
    The_app().run()
