import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from djitellopy import Tello

from code_python.global_function import is_wifi_drones_connected


class Better_Telo(Tello):
    _is_connected = None

    @property
    def is_connected(self):
        return self._is_connected

    @is_connected.setter
    def is_connected(self, value: bool):
        self._is_connected = value


class Better_Drone_Kit:
    def __init__(self):
        self.drone_adress = ""  # ENTRER ICI L'ADRESSE DU DRONE DE DRONE_KIT


class Drone_manager:
    def __init__(self) -> None:
        self.drone_tello = Better_Telo()
        self.drone_tello.is_connected = False
        self._is_connected = False
        self.current_drone = "Tello"

        self._drones = {"Tello": self.drone_tello, "Drone_Kit": None}


    @property
    def drone(self):
        return self._drones[self.current_drone]

    @property
    def temph(self) -> int:
        """enoie une requet au drone donc molo sur l'appel^^"""
        return self._get_temph()

    @property
    def battery(self) -> int:
        """enoie une requet au drone donc molo sur l'appel^^"""
        return self._get_battery()

    @property
    def is_flying(self) -> bool:
        """return true si il vole, false si non"""
        return self.drone_tello.is_flying

    @property
    def is_connected(self):
        self._is_connected = self.drone_tello.is_connected
        return self._is_connected

    @is_connected.setter
    def is_connected(self, value: bool):
        self._is_connected = self.drone_tello.is_connected = value

    def main_loop(self, moove=[0, 0, 0, 0]):
        """main loop du drone"""
        if self.drone_tello.is_flying:
            self.drone_tello.send_rc_control(moove[0], moove[1], moove[2], moove[3])

    def connect(self) -> bool:
        """ se connecte au drone avec la méthode Tello.conect()"""
        if is_wifi_drones_connected():
            self.drone_tello.connect(False)
            self.drone_tello.set_video_fps(Tello.FPS_30)
            self.is_connected = True
            return True
        else:
            return False

    def _get_battery(self) -> int:
        """Get current battery percentage Returns:
    int: 0-100 or retrun -1 if the drone are not connected"""
        if self.is_connected:
            return self.drone_tello.get_battery()
        else:
            return -1

    def _get_temph(self):
        """Get average temperature Returns:
    float: average temperature (°C)
    -1 if the drone are not connected"""
        if self.is_connected:
            return self.drone_tello.get_temperature()
        else:
            return -1

    def start_streeming(self):
        """retrun True si le drone est connecté et si le streem a commencé false sinon"""
        if self.drone_tello.is_connected:
            try:
                self.drone_tello.set_video_bitrate(0)
                self.drone_tello.streamon()
                return True
            except Exception as e:
                print(e)
                return False
        return False

    def get_image(self, image: Image) -> Image:
        """hpy : get les images a partit de Tello.get_frame_read() puis les transphorme en kivy.texture.Texture puis en kivy.image.Image"""
        frame_read = self.drone_tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (image.parent.width, image.parent.height))

        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        # ------------- convertie l'image en kivy.image.Image ------------- #
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='rgb')
        texture.blit_buffer(img.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        image.texture = texture
        image.canvas.ask_update()
        return image

    def stop_streeming(self):
        self.drone_tello.streamoff()

    def stop(self):
        self.drone_tello.end()


DRONE = Drone_manager()
