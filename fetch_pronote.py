import os
import sys
import csv
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
        # Tente de se connecter avec l'ENT
        client = pronotepy.Client(PRONOTE_URL, username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD, ent="educonnect")
    except Exception as e:
        print("Erreur connexion Pronote:", e)
        sys.exit(1)

    if not client.logged_in:
        print("❌ Échec connexion Pronote — vérifiez URL/identifiants ou que Pronote n'utilise pas une connexion CAS spécifique.")
        sys.exit(1)

    filename = "emploi.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "start_time", "end_time", "subject", "room", "teacher"])

        today = date.today()
        for day_offset in range(7):
            d = today + timedelta(days=day_offset)
            try:
                timetable = client.get_lessons(d)
            except Exception as e:
                print(f"Erreur récupération cours pour {d.isoformat()} :", e)
                timetable = []
            
            for lesson in timetable:
                # Vérifie si la leçon a des attributs start, end, etc. et gère les cas où ils sont des chaînes de caractères
                start = lesson.start.strftime("%H:%M") if getattr(lesson, "start", None) and not isinstance(lesson.start, str) else ""
                end   = lesson.end.strftime("%H:%M")   if getattr(lesson, "end", None) and not isinstance(lesson.end, str) else ""
                
                subject_obj = getattr(lesson, "subject", None)
                subject = subject_obj.name if subject_obj and not isinstance(subject_obj, str) else subject_obj if isinstance(subject_obj, str) else ""

                room_obj = getattr(lesson, "classroom", None)
                room = room_obj if isinstance(room_obj, str) else room_obj.name if room_obj else ""
                
                teacher_obj = getattr(lesson, "teacher", None)
                teacher = teacher_obj.name if teacher_obj and not isinstance(teacher_obj, str) else teacher_obj if isinstance(teacher_obj, str) else ""

                writer.writerow([d.isoformat(), start, end, subject, room, teacher])

    print("✅ emploi.csv généré.")

if __name__ == "__main__":
    main()
