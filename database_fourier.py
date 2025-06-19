import psycopg2
import os
from dotenv import load_dotenv

# .env-Datei laden für DB-Verbindung
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

# Verbindung herstellen
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Tabelle für Fourier-Fragetyp erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS fourier_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    image_path TEXT NOT NULL,
    hint TEXT NOT NULL,
    tip TEXT NOT NULL,
    a0_answer TEXT NOT NULL,
    a0_explanation TEXT NOT NULL,
    ak_answer TEXT NOT NULL,
    ak_explanation TEXT NOT NULL,
    bk_answer TEXT NOT NULL,
    bk_explanation TEXT NOT NULL
)
""")

# Beispiel-Datensatz einfügen
cursor.execute("""
INSERT INTO fourier_questions (
    question, image_path, hint, tip,
    a0_answer, a0_explanation,
    ak_answer, ak_explanation,
    bk_answer, bk_explanation
) VALUES (
    'Bestimmen Sie die Fourierreihe der mit der Periode 2 fortgesetzten Dreieckfunktion in reeller Darstellung:',
    'pictures_for_questions/fourier.png',
    'Die dargestellte Dreieckfunktion überschreitet aus Gründen der Übersichtlichkeit nur eine Periode.',
    'Überlegen Sie vorher genau, wie die Koeffizienten in etwa aussehen müssen.',
    '0,5',
    'Dies entspricht dem arithmetischen Mittel über eine Periode...',
    '...',
    'Durch partielle Integration...',
    '0',
    'Die Dreiecksfunktion ist gerade und enthält daher keine ungeraden Schwingungsanteile.'
)
""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("✅ Tabelle fourier_questions erfolgreich erstellt und Beispiel-Frage eingefügt.")