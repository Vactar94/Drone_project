from djitellopy import Tello
from inputs import get_key
from time import sleep
from ConnectAppManette import is_controller_connected

me = Tello()
me.connect()
print(me.get_battery())

flying = False  #suivre l'état de vol
micro_enabled = False  #suivre l'état du micro

def activer_microphone():
#utilisation de ChatGPT pour m'aider à la création de cette fonction car, n'ayant toujours pas le drône final nous ne sommes pas sûr de son utilisation et de son fonctionnement, cette fonctiones pûrement théorique
    global micro_enabled
    if not micro_enabled:
        #activer le microphone et envoyer le son au drone
        print("Microphone activé, le son est renvoyé par le drone.")
        micro_enabled = True

def getControllerInput():
    """ return une liste de 4 valeurs :
    [lr, fb, ud, yv]
    lr : axe gauche droite ()
    """
    if not is_controller_connected():
        return "Aucune manette reconnue"
    else:
        lr, fb, ud, yv = 0, 0, 0, 0
        speed = 50

        events = get_key()
        for event in events:
            if event.ev_type == 'Absolute':
                # droite/gauche
                if event.ev_code == 'ABS_X':
                    lr = int(event.ev_value / 32767.0 * speed)
                # devant/derrière
                elif event.ev_code == 'ABS_Y':
                    fb = int(event.ev_value / 32767.0 * speed)
                # haut/bas
                elif event.ev_code == 'ABS_Z':
                    ud = int(event.ev_value / 32767.0 * speed)
                # mouvement de rotation sur l'axe vertical
                elif event.ev_code == 'ABS_RZ':
                    yv = int(event.ev_value / 32767.0 * speed)
            elif event.ev_type == 'Key':
                if event.ev_code == 'BTN_SOUTH' and event.ev_value == 1:
                    # décoller/surplace, appuyer sur 'A'
                    global flying
                    if flying:
                        me.land()
                        flying = False
                    else:
                        me.takeoff()
                        flying = True
                elif event.ev_code == 'BTN_EAST' and event.ev_value == 1:
                    # Attérire, appuyer sur 'B'
                    me.land()
                    flying = False

                elif event.ev_code == 'BTN_WEST' and event.ev_value == 1:
                    # Activer/désactiver le micro, appuyer sur 'X'
                    if micro_enabled:
                        print("Microphone désactivé.")
                        micro_enabled = False
                    else:
                        activer_microphone()

            

        return [lr, fb, ud, yv]

if __name__ == "__main__" :
    while True:
        values = getControllerInput()
        me.send_rc_control(values[0], values[1], values[2], values[3])
        sleep(0.05)
