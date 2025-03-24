import os
import pickle
import platform
import uuid
import hashlib
from datetime import datetime

from fichier import design


def lire_param_gene():
    fichierini = "tabG"

    try:
        if os.path.isfile(fichierini):
            fichierSauvegarde = open(fichierini,"rb")
            variables = pickle.load(fichierSauvegarde)
            fichierSauvegarde.close()

            #Affichage de la liste
            lic = variables[1]
            return lic
        else:
            #Le fichier n'existe pas
            print("Fichier  non trouvé")
    except Exception as inst:
        design.logs("param_gene - "+str(inst))

def generate_activation_code():
    """Génère un code d'activation unique basé sur la machine de l'utilisateur"""
    machine_info = f"{platform.node()}{uuid.getnode()}{platform.processor()}"
    hashed = hashlib.sha256(machine_info.encode()).hexdigest()
    return f"ACT-{hashed[:16]}-{datetime.now().strftime('%y%m')}"


def verify_license():
    """Vérifie si une licence est valide"""
    secret_key = "Sruq_Opiwhjttil_Wtyxzllne"
    activation_code = generate_activation_code()
    license_key = lire_param_gene()
    import hmac
    from datetime import datetime

    try:
        if not license_key.startswith("LIC-") or len(license_key) != 45:
            print("Format de licence invalide")
            return False


        expiry_str = license_key.split('-')[1]
        expiry_date = datetime.strptime(expiry_str, "%Y%m%d")
        if datetime.now() > expiry_date:
            return False

        expected_signature = hmac.new(
            secret_key.encode(),
            activation_code.encode(),
            hashlib.sha256
        ).hexdigest()[:32]

        received_signature = license_key.split('-')[2]

        if not hmac.compare_digest(expected_signature, received_signature):
            return False
        else:
            return True

    except Exception as e:
        return False

