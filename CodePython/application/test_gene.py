from kivy.app import App
from kivy.uix.label import Label
from kivy.input.providers.hidinput import JoyButtonEvent, JoyAxisEvent

class JoystickApp(App):
    def build(self):
        self.label = Label(text="Appuyez sur un bouton de la manette.")
        return self.label

    def on_joy_button_down(self, window, stickid, buttonid):
        self.label.text = f"Bouton {buttonid} enfoncé!"

    def on_joy_button_up(self, window, stickid, buttonid):
        self.label.text = f"Bouton {buttonid} relâché."

    def on_joy_axis(self, window, stickid, axisid, value):
        self.label.text = f"Axe {axisid} déplacé à {value}"

if __name__ == '__main__':
    JoystickApp().run()

