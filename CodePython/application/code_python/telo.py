import cv2
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from djitellopy import Tello
from code_python.global_function import is_wifi_drones_connected
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
        self._is_connected = self.drone.is_connected = value

    


    def connect(self)-> bool :
        if is_wifi_drones_connected() :
            self.drone.connect(False)
            self.is_connected = True
            return True
        else : return False

    def get_battery(self)-> int :
        """Get current battery percentage Returns:
    int: 0-100 or retrun -1 if the drone are not connected"""
        if self.is_connected :
            return self.drone.get_battery()
        else :
            return -1
    
    def get_temph(self) :
        """Get average temperature Returns:
    float: average temperature (°C)
    -1 if the drone are not connected"""
        if self.is_connected :
            return self.drone.get_temperature()
        else : 
            return -1


    def start_streeming(self) :
        """retrun True si le drone est connecté et si le streem a commencé false sinon"""
        if self.drone.is_connected :
            try :
                self.drone.set_video_bitrate(0)
                self.drone.streamon()
                return True
            except Exception as e:
                print(e)
                return False
        return False


    def get_image(self,image:Image) -> Image :
        
            frame = self.drone.get_frame_read().frame
            frame = cv2.flip(frame, 0)  # Retournement vertical
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert the frame to a Kivy texture
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            image.texture = texture
            image.canvas.ask_update()
            return image

    def stop_streeming(self):
        self.drone.streamoff()

    def stop(self):
        self.drone.end()


DRONE = Drone_manager()