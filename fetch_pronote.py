# fetch_pronote.py
import os
import sys
from datetime import date, timedelta

try:
    import pronotepy
except Exception as e:
    print("Erreur import pronotepy:", e)
    sys.exit(1)

PRONOTE_URL = os.getenv("PRONOTE_URL")
PRONOTE_USERNAME = os.getenv("PRONOTE_USERNAME")
PRONOTE_PASSWORD = os.getenv("PRONOTE_PASSWORD")

if not (PRONOTE_URL and PRONOTE_USERNAME and PRONOTE_PASSWORD):
    print("Il manque une variable d'environnement (PRONOTE_URL / PRONOTE_USERNAME / PRONOTE_PASSWORD).")
    sys.exit(1)

def main():
    try:
        client = pronotepy.Client(PRONOTE_URL, username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD, ent="educonnect")
    except Exception as e:
        print("Erreur connexion Pronote:", e)
        sys.exit(1)

    if not client.logged_in:
        print("❌ Échec connexion Pronote — vérifiez URL/identifiants ou que Pronote n'utilise pas une connexion CAS spécifique.")
        sys.exit(1)

    print("✅ Connexion réussie à Pronote.")

    try:
        # Récupère les leçons pour aujourd'hui
        timetable = client.get_lessons(date.today())
        
        if not timetable:
            print("Aucune leçon trouvée pour aujourd'hui.")
            sys.exit(0)

        # Imprime la première leçon pour inspecter ses attributs
        first_lesson = timetable[0]
        print("\n--- Détails de la première leçon ---")
        print(f"Heure de début: {first_lesson.start}")
        print(f"Heure de fin: {first_lesson.end}")
        print(f"Matière: {first_lesson.subject}")
        print(f"Salle: {first_lesson.classroom}")
        print(f"Professeur: {first_lesson.teacher}")
        
    except Exception as e:
        print("Erreur lors de la récupération ou de l'impression des leçons:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
