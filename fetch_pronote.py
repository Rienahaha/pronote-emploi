# fetch_pronote.py
import os
import sys
import csv
from datetime import date, timedelta

# pronotepy peut lever des erreurs si le site Pronote a une connexion spéciale.
try:
    import pronotepy
except Exception as e:
    print("Erreur import pronotepy:", e)
    sys.exit(1)

# Variables d'environnement (configurées dans GitHub Secrets)
PRONOTE_URL = os.getenv("PRONOTE_URL")
PRONOTE_USERNAME = os.getenv("PRONOTE_USERNAME")
PRONOTE_PASSWORD = os.getenv("PRONOTE_PASSWORD")

if not (PRONOTE_URL and PRONOTE_USERNAME and PRONOTE_PASSWORD):
    print("Il manque une variable d'environnement (PRONOTE_URL / PRONOTE_USERNAME / PRONOTE_PASSWORD).")
    sys.exit(1)

def main():
    try:
        client = pronotepy.Client(PRONOTE_URL, username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD)
    except Exception as e:
        print("Erreur connexion Pronote:", e)
        sys.exit(1)

    if not client.logged_in:
        print("❌ Échec connexion Pronote — vérifie URL/identifiants ou que Pronote n'utilise pas une connexion CAS spécifique.")
        sys.exit(1)

    filename = "emploi.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "start_time", "end_time", "subject", "room", "teacher"])

        today = date.today()
        for day_offset in range(7):  # récupère la semaine à venir
            d = today + timedelta(days=day_offset)
            try:
                timetable = client.lessons(d)
            except Exception as e:
                print(f"Erreur récupération cours pour {d.isoformat()} :", e)
                timetable = []
            for lesson in timetable:
                start = lesson.start.strftime("%H:%M") if getattr(lesson, "start", None) else ""
                end   = lesson.end.strftime("%H:%M")   if getattr(lesson, "end", None) else ""
                subject = lesson.subject.name if getattr(lesson, "subject", None) and lesson.subject else ""
                room = lesson.classroom if getattr(lesson, "classroom", None) else ""
                teacher = lesson.teacher.name if getattr(lesson, "teacher", None) else ""
                writer.writerow([d.isoformat(), start, end, subject, room, teacher])

    print("✅ emploi.csv généré.")

if __name__ == "__main__":
    main()
