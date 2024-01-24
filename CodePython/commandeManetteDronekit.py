import time
import inputs
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk

# Connexion au drone
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)

vehicle.airspeed = 5 
vehicle.groundspeed = 7.5 

def décollage(altitude):

   while not vehicle.is_armable:
      print("En attente d'un drône prêt à l'armement")
      time.sleep(1)

   print("armement des moteurs")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True

   while not vehicle.armed: time.sleep(1)

   print("Décollage")
   vehicle.simple_takeoff(altitude)

   while True:
      v_alt = vehicle.location.global_relative_frame.alt
      print(">> Altitude = %.1f m"%v_alt)
      if v_alt >= altitude - 1.0:
          print("Altitude atteinte")
          break
      time.sleep(1)

def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html
    
    Bitmask to indicate which dimensions should be ignored by the vehicle 
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
    none of the setpoint dimensions should be ignored). Mapping: 
    bit 1: x,  bit 2: y,  bit 3: z, 
    bit 4: vx, bit 5: vy, bit 6: vz, 
    bit 7: ax, bit 8: ay, bit 9:
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> pris en compte seulement les vitesses
            0, 0, 0,        #-- position (x, y, z)
            vx, vy, vz,     #-- vélocité
            0, 0, 0,        #-- accélération
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


def control_drone_with_joystick():
    events = inputs.get_key()
    
    for event in events:
        if event.ev_type == 'Key':
            if event.ev_code == 'BTN_TRIGGER':
                # Le véhicule retourne en position de lancement lorsque BTN_TRIGGER est pressé
                vehicle.mav.command_long_send(
                    vehicle.target_system, vehicle.target_component,
                    mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                    0, 0, 0, 0, 0, 0, 0, 0, 0)

    js = inputs.devices.gamepads[0]
    events = js.read()

    for event in events:
        if event.ev_type == 'Absolute':
            scale_factor = 0.1 #-- à modifier en fonction du besoin
            if event.ev_type == 'ABS_X':
                vx = int(event.ev_value * scale_factor)
            elif event.ev_type == 'ABS_Y':
                vy = int(event.ev_value * scale_factor)
            elif event.ev_type == 'ABS_Z':
                vz = int(event.ev_value * scale_factor)

   
    set_velocity_body(vehicle, vx, vy, vz)#-- Ajuste la vélocité en fonction de l'entrée de la manette

