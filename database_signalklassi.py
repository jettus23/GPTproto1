import psycopg2
import os
from dotenv import load_dotenv

# .env-Datei laden für DB-Verbindung
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

# Verbindung herstellen
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Tabelle für Signalklassi-Fragetyp erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS signalklassi_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    input1 TEXT NOT NULL,
    input2 TEXT NOT NULL,
    input3 TEXT NOT NULL,
    input4 TEXT NOT NULL,
    input5 TEXT NOT NULL,
    input6 TEXT NOT NULL,
    input7 TEXT NOT NULL,
    image1 TEXT NOT NULL,
    image2 TEXT NOT NULL,
    image3 TEXT NOT NULL,
    image4 TEXT NOT NULL,
    image5 TEXT NOT NULL
)
""")

# Beispiel-Datensatz einfügen
cursor.execute("""
INSERT INTO signalklassi_questions (
    question,
    input1, input2, input3, input4, input5, input6, input7,
    image1, image2, image3, image4, image5
) VALUES (
    'Ordnen Sie die folgenden Signalformen den richtigen Kategorien zu.',
    'Stochastisch', 'Nichtstationär', 'Stationär', 'Deterministisch', 'Quasiperiodisch', 'Nicht-periodisch', 'Periodisch',
    'pictures_for_questions/signal1.png',
    'pictures_for_questions/signal2.png',
    'pictures_for_questions/signal3.png',
    'pictures_for_questions/signal4.png',
    'pictures_for_questions/signal5.png'
)
""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("✅ Tabelle signalklassi_questions erfolgreich erstellt und Beispiel-Frage eingefügt.")
