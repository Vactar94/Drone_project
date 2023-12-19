from kivy.app import App
from kivy.uix.image import Image 
from kivy.uix.button import Button 
from kivy.uix.relativelayout import RelativeLayout 
from kivy.graphics.texture import Texture
import cv2

from kivy.clock import Clock 
from kivy.core.window import Window
from djitellopy import Tello
DRONE = Tello()

Window.size = [360, 620]
class Test_Streem_App(App):
    def build(self):

        self.button_land = Button(text="atterrir",size_hint=(None, None), size=[200,100],pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.button_takeoff = Button(text="s'envoler",size_hint=(None, None), size=[200,100],pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.button_connect = Button(text="connect",size_hint=(None, None), size=[200,100],pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.button_takeoff.bind(on_release=self.takeoff)
        self.button_land.bind(on_release=self.land)
        self.button_connect.bind(on_release=self.connect)
        box = RelativeLayout(size=Window.size)

        self.backgroud = Image(size=box.size)



        box.add_widget(self.backgroud)
        box.add_widget(self.button_land)
        box.add_widget(self.button_takeoff)
        box.add_widget(self.button_connect)
       

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        
        return box

    def update(self,dt):
        if DRONE.stream_on :
            self.backgroud = self.get_image(self.backgroud)

    def land(self,value) :
        if DRONE.is_flying :
            DRONE.land()
        else :
            DRONE.streamoff()

    def takeoff(self,value) :
        if not DRONE.is_flying :
            DRONE.takeoff()

    def connect(self,value) :
        DRONE.connect()

        print("go to streem")
        self.start_streeming()
        print("back to streem")


    def start_streeming(self):
        DRONE.streamon()
        DRONE.set_video_fps(Tello.FPS_30)



    def get_image(self,image:Image) -> Image :
        
            frame = DRONE.get_frame_read().frame
            frame = cv2.flip(frame, 0)  # Retournement vertical

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert the frame to a Kivy texture
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            image.texture = texture
            image.canvas.ask_update()
            return image
    

if __name__ == '__main__':
    DRONE.connect()
    print(DRONE.get_battery())

