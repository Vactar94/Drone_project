from code_python.global_function import is_controller_connected
from code_python.notification import NOTIF_MANAGER
from threading import Thread

from code_python.langues.langues import UPDATE_MANAGER


class Controller:
    _is_connected = False
    @property
    def is_connected(self):
        return self._is_connected
    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = value
        if value:
            NOTIF_MANAGER.Waiting_notifications["M"][1] = True
            UPDATE_MANAGER.update_all_controller(value)
        elif not value:
            NOTIF_MANAGER.Waiting_notifications["M"][0] = True
            UPDATE_MANAGER.update_all_controller(value)


    def try_connectivity(self):
        Thread(target=is_controller_connected, args=(self,)).start()


CONTOLLER = Controller()