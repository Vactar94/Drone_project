from djitellopy import Tello
from inputs import get_key
from time import sleep

me = Tello()
me.connect()
print(me.get_battery())

def getControllerInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    events = get_key()
    for event in events:
        if event.ev_type == 'Absolute':
            #droite/gauche
            if event.ev_code == 'ABS_X':
                lr = int(event.ev_value / 32767.0 * speed)
            #devant/derrière
            elif event.ev_code == 'ABS_Y':
                fb = int(event.ev_value / 32767.0 * speed)
            #haut/bas
            elif event.ev_code == 'ABS_Z':
                ud = int(event.ev_value / 32767.0 * speed)
            #mouvement de rotation sur l'axe vertical
            elif event.ev_code == 'ABS_RZ':
                yv = int(event.ev_value / 32767.0 * speed)
# Voler sur place/décoller          
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
                # Attérire, appuyer sur 'B
                me.land()
                flying = False

    return [lr, fb, ud, yv]

while True:
    values = getControllerInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])
    sleep(0.05)
