from plyer import wifi
import platform
import bluetooth


def discover_devices():
    devices = bluetooth.discover_devices(lookup_names=True)
    return devices

def main():
    try:
        devices = discover_devices()
        print("Appareils Bluetooth connectés :")
        for addr, name in devices:
            print(f"{name} ({addr})")
    except bluetooth.btcommon.BluetoothError as e:
        print(f"Erreur Bluetooth : {e}")



def is_controller_connected():
    device_address = '00:00:00:00:00:00'  # mettre l'adresse de la manette
    device_name = ['Xbox Wireless Controller','Controller','controller','Pro Controller', 'pro controller', 'Pro controller', 'pro Controller']
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True, device_id=-1)
    

    for addr, name, _ in nearby_devices:
        if  name in device_name:
            return True

    return False

def is_drones_connected():

    if wifi == 'connected':
        wifi_name = wifi.available_ssids()
        if "TELLO-dronensi" in wifi_name:
              return True
        else:
            return False
    else : 
        return False
    
def det_sys():
    """determine dans quelle OS on est return la première lettre de l'os :
        W : Windows
        L : Linux
        M : MacOs
        A : Android
        Z : OS non reconue
    """

    system = platform.system()  # Récupère le nom du système d'exploitation
    release = platform.release()  # Récupère la version du système d'exploitation

    print(f"Système d'exploitation : {system}")
    print(f"Version : {release}")

    if system == "Windows":                                                         return "W"
    elif system == "Linux":                                                         return "L"
    elif system == "Darwin":                                                        return "M"
    elif platform.system() == "Linux" and "android" in platform.platform().lower(): return "A"
    else :                                                                          return "Z"
