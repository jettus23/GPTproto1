import psycopg2
import os
from dotenv import load_dotenv

# .env-Datei laden für DB-Verbindung
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

# Verbindung herstellen
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Neue Tabelle für Parallelitätabc
cursor.execute("""
CREATE TABLE IF NOT EXISTS parallelitaetabc_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    step1_prompt TEXT NOT NULL,
    step1_ideal TEXT NOT NULL,
    step2_prompt TEXT NOT NULL,
    step2_ideal TEXT NOT NULL,
    step3_prompt TEXT NOT NULL,
    step3_ideal TEXT NOT NULL,
    step4_prompt TEXT NOT NULL,
    step4_ideal TEXT NOT NULL
)
""")

# Beispiel-Datensatz einfügen
cursor.execute(
    "INSERT INTO parallelitaetabc_questions (question, step1_prompt, step1_ideal, step2_prompt, step2_ideal, step3_prompt, step3_ideal, step4_prompt, step4_ideal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (
        "Recherchieren Sie zur Vorbereitung auf diese Aufgabe zunächst Amdahls Gesetz und Gustafsons Gesetz!",
        "Formel eingeben:",
        "S = 1 / ((1 - P) + o(N) + (P / N)) ≤ 1 / (1 - P)",
        "Erläutern Sie die Bedeutung der Variablen, die in der Formel benötigt werden:",
        "P: Parallelisierbarer Anteil der Gesamtaufgabe.\nN: Anzahl der zur Verfügung stehenden Prozessoren.\no(N): Zeitaufwand (Kosten), der durch Synchronisation u.ä. anfällt und nicht zur Bearbeitung der Aufgabe verwendet werden kann.",
        "b) Fassen Sie die Aussage(n) von Amdahls Gesetz in eigenen Worten zusammen!",
        "Amdahls Gesetz besagt, dass der serielle Anteil eines Programms die durch Parallelisierung maximal erreichbare Beschleunigung begrenzt. Selbst mit unendlich vielen Prozessoren bleibt eine gewisse Laufzeit notwendig.",
        "c) Welche Schwachstellen hat Amdahls Gesetz?",
        "Das Gesetz berücksichtigt nicht, dass weitere beschleunigende Elemente wie z. B. Caches existieren. Es geht von einer festen Problemgröße aus und berücksichtigt nicht, dass durch Parallelisierung ggf. komplexere Probleme lösbar werden."
    )
)

# Änderungen speichern & Verbindung schließen
conn.commit()
conn.close()

print("✅ Tabelle parallelitaetabc_questions erfolgreich erstellt und Beispiel-Frage eingefügt.")
