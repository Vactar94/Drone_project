from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import time
from queue import Queue

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.button = Button(text='Exécuter la fonction')
        self.label = Label(text='')

        self.button.bind(on_press=self.execute_function)

        self.layout.add_widget(self.button)
        self.layout.add_widget(self.label)

        self.result_queue = Queue()  # Queue pour stocker le résultat de la fonction

        return self.layout

    def execute_function(self, instance):
        # Désactive le bouton pendant l'exécution de la fonction
        self.button.disabled = True

        # Lance la fonction dans un thread séparé
        threading.Thread(target=self.long_running_function, args=(self.result_queue,)).start()

        # Planifie une mise à jour régulière pour vérifier si la fonction est terminée
        Clock.schedule_interval(self.check_function_status, 1.0)

    def long_running_function(self, result_queue):
        # Fonction qui prend du temps
        time.sleep(5)

        # Résultat de la fonction
        result = "Résultat de la fonction"

        # Mettez le résultat dans la queue
        result_queue.put(result)

    def check_function_status(self, dt):
        if threading.active_count() == 1:
            # Aucun thread en cours d'exécution, la fonction est terminée
            if not self.result_queue.empty():
                result = self.result_queue.get()
                self.label.text = f'Résultat: {result}'
            else:
                self.label.text = 'Fonction terminée sans résultat'

            self.button.disabled = False
            # Arrête le contrôle régulier
            Clock.unschedule(self.check_function_status)

if __name__ == '__main__':
    a = Queue(52)
    a = "w"
    print(a)
