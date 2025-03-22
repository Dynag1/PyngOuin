import platform
import uuid
import hashlib
from datetime import datetime


def generate_activation_code():
    """Génère un code d'activation unique basé sur la machine de l'utilisateur"""
    machine_info = f"{platform.node()}{uuid.getnode()}{platform.processor()}"
    hashed = hashlib.sha256(machine_info.encode()).hexdigest()
    return f"ACT-{hashed[:16]}-{datetime.now().strftime('%y%m')}"


def verify_license(license_key, activation_code):
    """Vérifie si une licence est valide"""
    secret_key = "Sruq_Opiwhjttil_Wtyxzllne"
    import hmac
    from datetime import datetime

    try:
        if not license_key.startswith("LIC-") or len(license_key) != 45:
            return False, "Format de licence invalide"

        expiry_str = license_key.split('-')[1]
        expiry_date = datetime.strptime(expiry_str, "%Y%m%d")
        if datetime.now() > expiry_date:
            return False, "Licence expirée"

        expected_signature = hmac.new(
            secret_key.encode(),
            activation_code.encode(),
            hashlib.sha256
        ).hexdigest()[:32]

        received_signature = license_key.split('-')[2]

        if not hmac.compare_digest(expected_signature, received_signature):
            return False, "Signature de licence invalide"

        return True, "Licence valide"

    except Exception as e:
        return False, f"Erreur lors de la vérification : {str(e)}"


# Utilisation côté client
if __name__ == "__main__":
    SECRET_KEY = "votre_cle_secrete_super_securisee_123!"  # Devrait être le même que sur le serveur

    # Étape 1 : Générer le code d'activation
    activation_code = generate_activation_code()
    print(f"Votre code d'activation est : {activation_code}")
    print("Envoyez ce code au serveur pour obtenir votre licence.")

    # Étape 2 : Attendre que l'utilisateur entre la licence
    license_key = input("Entrez la licence reçue du serveur : ")

    # Étape 3 : Vérifier la licence
    is_valid, message = verify_license(license_key, activation_code)
    print(f"Résultat de la vérification : {message}")
