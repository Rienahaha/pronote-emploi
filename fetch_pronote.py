# fetch_pronote.py
import os
import sys

try:
    import pronotepy
except Exception as e:
    print("Erreur import pronotepy:", e)
    sys.exit(1)

# Variables d'environnement
PRONOTE_URL = os.getenv("PRONOTE_URL")
PRONOTE_USERNAME = os.getenv("PRONOTE_USERNAME")
PRONOTE_PASSWORD = os.getenv("PRONOTE_PASSWORD")

if not (PRONOTE_URL and PRONOTE_USERNAME and PRONOTE_PASSWORD):
    print("Il manque une variable d'environnement (PRONOTE_URL / PRONOTE_USERNAME / PRONOTE_PASSWORD).")
    sys.exit(1)

def main():
    try:
        # Tente de se connecter avec l'ENT
       client = pronotepy.Client(PRONOTE_URL, username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD)
    except Exception as e:
        print("Erreur connexion Pronote:", e)
        sys.exit(1)

    if not client.logged_in:
        print("❌ Échec connexion Pronote — vérifiez URL/identifiants ou que Pronote n'utilise pas une connexion CAS spécifique.")
        sys.exit(1)
    
    print("✅ Connexion réussie à Pronote.")

if __name__ == "__main__":
    main()
