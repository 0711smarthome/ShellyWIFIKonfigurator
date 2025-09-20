import sys
import time
import requests
from pydbus import SystemBus

def find_shelly_ap():
    """
    Sucht nach Shelly APs mithilfe der D-Bus-API des NetworkManager.
    """
    try:
        bus = SystemBus()
        network_manager = bus.get("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")

        # Scan-Anfrage senden und 5 Sekunden auf Ergebnisse warten
        network_manager.RequestScan({'type': '802-11-wireless', 'ssid': ''})
        time.sleep(5) 

        # Liste der Access Points abrufen
        access_points_paths = network_manager.GetAllAccessPoints()
        
        for ap_path in access_points_paths:
            ap_proxy = bus.get("org.freedesktop.NetworkManager", ap_path)
            # D-Bus-Objekt Eigenschaft 'Ssid' abrufen (im Bytes-Format)
            ssid_bytes = ap_proxy.Ssid
            ssid = ssid_bytes.decode('utf-8')

            if ssid.startswith('shelly'):
                print(f"Shelly AP gefunden: {ssid}")
                return ssid_bytes
        
        print("Kein Shelly AP gefunden.")
        return None
    except Exception as e:
        print(f"Fehler bei der D-Bus-Suche: {e}")
        return None

def connect_to_shelly(ssid_bytes):
    """
    Verbindet sich mit dem Shelly AP über D-Bus.
    """
    try:
        bus = SystemBus()
        network_manager = bus.get("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        
        # Verbindungsprofil für den Shelly erstellen
        connection_settings = {
            '802-11-wireless': {
                'ssid': ssid_bytes,
                'mode': 'ap', # Der Shelly ist im AP-Modus
            },
            'connection': {
                'type': '802-11-wireless',
                'id': 'shelly_ap_temp',
            }
        }
        
        # Verbindung aktivieren
        active_connection = network_manager.AddAndActivateConnection(
            connection_settings,
            '/org/freedesktop/NetworkManager/Devices/0', # Dieser Pfad kann variieren, aber meistens ist 0 der WLAN-Adapter
            '/org/freedesktop/NetworkManager/Settings/0'
        )
        
        time.sleep(15)
        print("Verbindung zum Shelly AP hergestellt.")
        return True
    except Exception as e:
        print(f"Verbindung fehlgeschlagen: {e}")
        return False

def configure_shelly(wifi_ssid, wifi_password):
    """
    Sendet die WLAN-Konfiguration an den Shelly per HTTP-Request.
    """
    shelly_ip = "http://192.168.33.1"
    url = f"{shelly_ip}/settings/sta?ssid={wifi_ssid}&key={wifi_password}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Shelly erfolgreich konfiguriert!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Konfiguration: {e}")
        return False

def restore_network():
    """
    Stellt die ursprüngliche Netzwerkverbindung wieder her.
    """
    try:
        bus = SystemBus()
        network_manager = bus.get("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        
        # Alle aktiven Verbindungen abrufen und unsere temporäre deaktivieren
        active_connections_paths = network_manager.ActiveConnections
        for conn_path in active_connections_paths:
            conn_proxy = bus.get("org.freedesktop.NetworkManager", conn_path)
            connection_properties = conn_proxy.Get(
                'org.freedesktop.NetworkManager.Connection.Active',
                'Id'
            )
            if connection_properties == 'shelly_ap_temp':
                network_manager.DeactivateConnection(conn_path)
                print("Temporäre Shelly-Verbindung getrennt.")
                break
        
        time.sleep(15)
        print("Netzwerk wiederhergestellt.")
    except Exception as e:
        print(f"Fehler bei der Wiederherstellung: {e}")

def main(your_wifi_ssid, your_wifi_password):
    shelly_ssid_bytes = find_shelly_ap()
    
    if not shelly_ssid_bytes:
        return

    if not connect_to_shelly(shelly_ssid_bytes):
        return
        
    if not configure_shelly(your_wifi_ssid, your_wifi_password):
        restore_network()
        return

    restore_network()
    print("Vorgang abgeschlossen.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Fehler: SSID und Passwort müssen als Argumente übergeben werden.")
        sys.exit(1)
        
    HOME_WIFI_SSID = sys.argv[1]
    HOME_WIFI_PASS = sys.argv[2]
    
    main(HOME_WIFI_SSID, HOME_WIFI_PASS)
