import os
import platform
import bluetooth
import psutil
import subprocess
from jnius import autoclass


def main():
    try:
        devices = bluetooth.discover_devices(lookup_names=True)
        print("Appareils Bluetooth connectés :")
        for addr, name in devices:
            print(f"{name} ({addr})")
    except bluetooth.btcommon.BluetoothError as e:
        print(f"Erreur Bluetooth : {e}")

def is_controller_connected(value=None)->bool:
    """return True si il y a un controler de connected"""
    print("device_name")
    device_name = ["Xbox", "Controler","Xbox Wireless Contoller"]
    print("nearby_devices")

    nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True)
    print("bouvle for")
    print(nearby_devices)
    for _, name in nearby_devices:
        print(name)
        for name_possible in device_name :
            if name in name_possible:
                if value !=None :
                    value.is_controller_connected = True
                return True
    if value !=None :
        value.is_controller_connected = False
    return False



# fonctions pour savoir si wifi est propre a envoyer des paquet au drone #
def is_wifi_drones_connected():
    """determine si l'ordinateur est connecté au résaux pour le drone"""
    # Exécutez une commande pour obtenir la liste des réseaux Wi-Fi disponibles
    result = get_connected_wifi_name_windows()
    # Recherchez le nom du réseau "TELLO-dronensi" dans le résultat
    
    list_name_drone = ["TELLO", "Drone", "DRONE", "Tello"]
    for name_wifi_possible in list_name_drone :  
        if name_wifi_possible in result :
            return True
    return False


def get_connected_wifi_name_windows()->str:
    """determination du nom du wifi qui est acutellement connecté pour pouvoir l'utiliser après."""
    if SYSTEM == "W":
        try:
            result = os.popen('netsh wlan show interfaces | findstr "SSID"').read()
            # Analyse le résultat pour obtenir le nom du réseau
            ssid_line = [line for line in result.split('\n') if 'SSID' in line]
            if ssid_line:
                ssid = ssid_line[0].split(":")[1].strip()
                return ssid
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
    elif SYSTEM == "L" :
        pass
    elif SYSTEM == "A" :
        pass
    return ""

def det_sys():
    """determine dans quelle OS on est return la première lettre de l'os :
        W : Windows
        L : Linux
        M : MacOs
        A : Android
        Z : OS non reconue
    """
    system = platform.system()  # Récupère le nom du système d'exploitation
    if system == "Windows":                                                         return "W"
    elif system == "Linux":                                                         return "L"
    elif system == "Darwin":                                                        return "M"
    elif platform.system() == "Linux" and "android" in platform.platform().lower(): return "A"
    else :                                                                          return "Z"


def get_battery_ordinateur()-> int :
    """getter pour la batterie du telephone/ordinateur
    la batterie est en poursent mais si elle dépasse 100 c'est que elle est branché"""
    if SYSTEM == 'W':
        battery = psutil.sensors_battery()
        if battery.power_plugged :
            b = battery.percent + 100
        else :
            b = battery.percent
        return b
    elif SYSTEM == "L" :
        return get_linux_batt()
    elif SYSTEM == "A" :
        return get_battery_info()



def get_linux_batt()->int:

    try:
        # Utilise la commande upower pour obtenir des informations sur la batterie
        result = subprocess.run(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], capture_output=True, text=True)

        # Analyse la sortie pour obtenir les informations nécessaires
        lines = result.stdout.split('\n')
        for line in lines:
            if 'percentage' in line:
                percent = line.split(':')[1].strip()
                print(f"Niveau de batterie : {percent}")
            elif 'state' in line:
                state = line.split(':')[1].strip()
                print(f"État de la batterie : {state}")
        
        

    except Exception as e:
        print(f"Erreur : {e}")





def get_battery_info()-> int:
    Context = autoclass('android.content.Context')
    BatteryManager = autoclass('android.os.BatteryManager')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    battery_manager = activity.getSystemService(Context.BATTERY_SERVICE)
    # Obtient le niveau de batterie actuel
    level = battery_manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)

    # Obtient l'état actuel de la batterie (branchée ou débranchée)
    plugged = battery_manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_PLUGGED)
    is_plugged = plugged != 0

    if is_plugged : return level + 100
    else :          return level

SYSTEM = det_sys()


def get_connected_devices():
    # Recherche des appareils Bluetooth
    nearby_devices = bluetooth.discover_devices(lookup_names=True, device_id=-1, duration=8, lookup=True)

    # Liste des appareils connectés
    connected_devices = []

    for addr, name in nearby_devices:
        if bluetooth.lookup_name(addr, device_id=-1, lookup=True) is not None:
            connected_devices.append({"address": addr, "name": name})

    return connected_devices

if __name__ == "__main__" :

    connected_devices = get_connected_devices()

    if not connected_devices:
        print("Aucun appareil Bluetooth connecté.")
    else:
        print("Appareils Bluetooth connectés:")
        for device in connected_devices:
            print(f"Adresse: {device['address']}, Nom: {device['name']}")