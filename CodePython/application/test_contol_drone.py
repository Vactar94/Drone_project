from djitellopy import Tello
import time
d = Tello()

d.connect()



print("decolage")

print(d.get_battery())
d.takeoff()




print("atterisage")
d.land()
d.end()

