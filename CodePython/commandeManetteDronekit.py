from dronekit import connect, VehicleMode
import pygame
import time

# Connexion au drone
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)

# Initialisation de Pygame
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Fonction pour normaliser les valeurs de la manette
def normalize_input(value, deadzone=0.05):
    if abs(value) < deadzone:
        return 0.0
    elif value > 0:
        return (value - deadzone) / (1.0 - deadzone)
    else:
        return (value + deadzone) / (1.0 - deadzone)

try:
    while True:
        pygame.event.get()

        # Lire les axes de la manette
        h_dg = normalize_input(joystick.get_axis(0))#droite/gauche horizontale
        dd = normalize_input(joystick.get_axis(1))#devant/derrière
        hb = normalize_input(-joystick.get_axis(5))#haut/bas
        v_dg = normalize_input(joystick.get_axis(4))#droite/gauche verticale

        vehicle.channels.overrides = {
            '1': int(1500 + v_dg * 500),    
            '2': int(1500 + dd * 500),   
            '3': int(1500 + h_dg * 500), 
            '4': int(1500 + hb * 500)     
        }

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Arrêt du programme.")
finally:
    # Réinitialiser les canaux de contrôle à la fin
    vehicle.channels.overrides = {}
    vehicle.close()
    pygame.joystick.quit()
    pygame.quit()
