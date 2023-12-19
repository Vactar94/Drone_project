import os
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



def chec_controller_connected(is_controller_connected):
    device_address = '00:00:00:00:00:00'  # mettre l'adresse de la manette
    device_name = ['Xbox Wireless Controller','Controller','controller','Pro Controller', 'pro controller', 'Pro controller', 'pro Controller']
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True, device_id=-1)
    

    for addr, name, _ in nearby_devices:
        if  name in device_name:
            is_controller_connected = True
            return True

    is_controller_connected = False



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
    """determination du nom du wifi pour pouvoir l'utiliser après."""
    if det_sys() == "W":
        try:
            result = os.popen('netsh wlan show interfaces | findstr "SSID"').read()
            # Analyse le résultat pour obtenir le nom du réseau
            ssid_line = [line for line in result.split('\n') if 'SSID' in line]
            if ssid_line:
                ssid = ssid_line[0].split(":")[1].strip()
                return ssid
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
    elif det_sys() == "L" :
        pass
    elif det_sys() == "A" :
        pass
    return None

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

if __name__ == "__main__" :
    print(get_connected_wifi_name_windows())

