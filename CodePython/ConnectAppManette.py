import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import wifi
import bluetooth

kivy.require('1.11.1')

def is_drones_connected():
    if wifi == 'connected':
        wifi_name = wifi.available_ssids()
        if "TELLO-dronensi" in wifi_name:
              return True
        else:
            return False
    else : 
        return False

def is_controller_connected():
    device_name = 'Xbox Wireless Controller'
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True)

    for _, name, _ in nearby_devices:
        if name == device_name:
            return True

    return False


class MyApp(App):
    def build(self):

        controller_connected = is_controller_connected()
        drone_connected = is_drones_connected()
        if controller_connected:
            message1 = 'Manette connectée'
        else:
            message1 = 'Manette non connectée'
        
        if drone_connected:
            message2=' Drone connecté'
        else:
            message2 = ' Drone non connecté'

        return Label(text=message1+message2)



if __name__ == '__main__':
    MyApp().run()