import psycopg2
import os
from dotenv import load_dotenv

# .env-Datei laden für DB-Verbindung
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

# Verbindung herstellen
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Tabelle für Abtastungs-Fragetyp erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS abtastung_questions (
    id SERIAL PRIMARY KEY,
    intro TEXT NOT NULL,
    teil1_prompt TEXT NOT NULL,
    teil2_prompt TEXT NOT NULL,
    teil1_answer TEXT NOT NULL,
    teil1_unit TEXT NOT NULL,
    teil1_explanation TEXT NOT NULL,
    teil2_answer TEXT NOT NULL,
    teil2_unit TEXT NOT NULL,
    teil2_explanation TEXT NOT NULL
)
""")

# Beispiel-Datensatz einfügen
cursor.execute("""
INSERT INTO abtastung_questions (
    intro, teil1_prompt, teil2_prompt,
    teil1_answer, teil1_unit, teil1_explanation,
    teil2_answer, teil2_unit, teil2_explanation
) VALUES (
    'Gegeben sei eine periodische Schwingung der Frequenz f₀ = 10 Hz. Die Schwingung wird beschrieben durch f(x) = A · sin(2πf₀t). Diese Schwingung soll nun abgetastet werden.',
    'Wie groß muss die Abtastfrequenz fₐ mindestens sein, damit das Signal fehlerfrei aus den Abtastwerten wiederhergestellt werden kann?',
    'Das Signal wird nun mit der Frequenz fₐ = 15 Hz abgetastet. Welche Frequenz fᵣ hat die Schwingung, die aus den Abtastwerten rekonstruiert wird?',
    '20', 'Hz',
    'Das Abtasttheorem besagt, dass ein Signal mit mehr als der doppelten im Signal maximal auftretenden Frequenz abgetastet werden muss, um dieses fehlerfrei rekonstruieren zu können. Die maximale (und einzige) Frequenz, die im Signal auftritt, ist 10 Hz, also muss die Abtastfrequenz über 20 Hz liegen.',
    '5', 'Hz',
    'Der Effekt lässt sich am einfachsten an einer Grafik erläutern: Im oberen Teil ist die Originalschwingung dargestellt (10 Hz entspricht einer Periodendauer von 100 ms). An denjenigen Stellen, wo ein Kreuz eingezeichnet ist, wird mit 15 Hz (alle 1/15 Sekunde, also alle 66,66 ms) abgetastet. Der untere Bildteil stellt zwischen diesen Abtastpunkten interpolierte Schwingung dar (Rekonstruktion). Diese hat erkennbar eine Periodendauer von 200 ms, d.h. eine Frequenz von 5 Hz.'
)
""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("✅ Tabelle abtastung_questions erfolgreich erstellt und Beispiel-Frage eingefügt.")
