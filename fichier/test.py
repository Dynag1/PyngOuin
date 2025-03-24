import socket
import re
from urllib.parse import urlparse


def decouvrir_appareils_upnp(timeout=5):
    """
    Découvre les appareils UPnP sur le réseau local en utilisant SSDP
    Retourne une liste de dictionnaires contenant les informations des appareils
    """
    # Message de découverte SSDP
    message = \
        'M-SEARCH * HTTP/1.1\r\n' \
        'HOST: 239.255.255.250:1900\r\n' \
        'MAN: "ssdp:discover"\r\n' \
        'MX: 2\r\n' \
        'ST: ssdp:all\r\n' \
        '\r\n'

    # Configuration du socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.settimeout(timeout)

    # Envoi du message de découverte
    sock.sendto(message.encode('utf-8'), ('239.255.255.250', 1900))

    appareils = []
    while True:
        try:
            data, addr = sock.recvfrom(65507)
            appareil = {
                'ip': addr[0],
                'port': addr[1]
            }

            # Extraction des informations de l'appareil
            for line in data.decode('utf-8').splitlines():
                if line.startswith('LOCATION:'):
                    appareil['location'] = line.split(':', 1)[1].strip()
                elif line.startswith('SERVER:'):
                    appareil['server'] = line.split(':', 1)[1].strip()
                elif line.startswith('ST:'):
                    appareil['type'] = line.split(':', 1)[1].strip()

            if 'location' in appareil:
                url = urlparse(appareil['location'])
                appareil['url'] = f"{url.scheme}://{url.netloc}"

            appareils.append(appareil)
        except socket.timeout:
            break

    sock.close()
    return appareils


# Utilisation de la fonction
appareils_trouves = decouvrir_appareils_upnp()
for appareil in appareils_trouves:
    print(f"Appareil UPnP trouvé : {appareil['ip']}:{appareil['port']}")
    print(f"  Type : {appareil.get('type', 'Non spécifié')}")
    print(f"  URL : {appareil.get('url', 'Non disponible')}")
    print(f"  Serveur : {appareil.get('server', 'Non spécifié')}")
    print("---")
