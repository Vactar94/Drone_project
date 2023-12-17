import cv2
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from djitellopy import Tello
import threading


class Better_Telo (Tello):
    _is_connected = None

    @property
    def is_connected(self) :
        return self._is_connected
    
    @is_connected.setter
    def is_connected(self,value:bool) :
        self._is_connected = value
        


class Drone_manager :
    def __init__(self) -> None:
        self.drone = Better_Telo()
        self.drone.is_connected = False
        self._is_connected = False
    

    @property
    def is_connected(self) :
        self._is_connected = self.drone.is_connected
        return self._is_connected
    
    @is_connected.setter
    def is_connected(self,value:bool) :
        self._is_connected = value
    


    def connect(self) :
        self.drone.connect(False)



    def start_streeming(self) :
        """retrun True si le drone est connecté et si le streem a commencé false sinon"""
        if self.drone.is_connected :
            try :
                self.drone.set_video_bitrate(0)
                self.drone.stream_on()
                return True
            except Exception as e:
                print(e)
                return False
        return False


    def get_image(self,image:Image) -> Image :
       
        frame = self.drone.get_frame_read().frame
        # Convert the frame to a Kivy texture
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

        image.texture = texture
        image.canvas.ask_update()
        return image

    def stop_streeming(self):
        # Release resources when the application is closed
        self.drone.streamoff()

    def stop(self):
        self.drone.end()


DRONE = Drone_manager()