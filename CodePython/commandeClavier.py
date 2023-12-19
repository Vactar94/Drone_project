from djitellopy import tello
import KeyPressModule as kp
from time import sleep

kp.init()
me=tello.tello()
me.connect()
print(me.get_battery())

def getKeyboardInput():
    lr,fb,ud,yv = 0, 0, 0, 0
    speed = 50
# droite/gauche
    if kp.getKey("q"):
        lr= -speed
    elif kp.getKey("d"):
        lr= speed
# devant/derrière
    elif kp.getKey("z"):
        fb= speed
    elif kp.getKey("s"):
        fb= -speed
# haut/bas
    elif kp.getKey("space"):
        ud= speed
    elif kp.getKey("ctrl"):
        ud= -speed
# vélocité
    elif kp.getKey("a"):
        yv= speed
    elif kp.getKey("e"):
        yv= -speed
    
    return [lr,fb,ud,yv]



while True:
    me.send_rc_control(0, 0, 0, 0)