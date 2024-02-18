from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        button = Button(text="Hello, upside down!")
        layout.add_widget(button)

        return layout


if __name__ == '__main__':
    MyApp().run()
