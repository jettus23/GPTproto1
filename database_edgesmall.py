import psycopg2
import os
from dotenv import load_dotenv

# .env-Datei laden für DB-Verbindung
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

# Verbindung herstellen
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Tabelle für EdgeSmall-Fragetyp erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS edge_small_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    subquestion_a TEXT NOT NULL,
    solution_a TEXT NOT NULL,
    explanation_a TEXT NOT NULL,
    subquestion_b TEXT NOT NULL,
    solution_b TEXT NOT NULL,
    explanation_b TEXT NOT NULL
)
""")

# Beispiel-Datensatz einfügen
cursor.execute("""
INSERT INTO edge_small_questions (
    question,
    subquestion_a,
    solution_a,
    explanation_a,
    subquestion_b,
    solution_b,
    explanation_b
) VALUES (
    'Gegeben sei ein Ring mit N=15 Knoten k₁, k₂, ..., k₁₅ und d=4. d.h. jeder Knoten ist nicht nur mit seinen direkten Nachbarn, sondern auch mit seinen jeweils übernächsten Nachbarn in beide Richtungen verbunden.',
    'Bestimmen Sie den Cluster-Koeffizienten für den Ring.',
    '0,5',
    'Jeder Knoten hat 4 direkte Nachbarn. Es gibt somit 6 mögliche bidirektionale Verbindungen. Davon sind 3 tatsächlich vorhanden. Der lokale Clust.koeff. ist 3/6 = 0,5, und da alle Knoten gleich sind, entspricht dies dem globalen Wert.',
    'Ermitteln Sie für den Knoten k₁ die mittlere Pfadlänge, indem Sie den Durchschnitt der Pfadlängen zu allen anderen Knoten bestimmen.',
    '16/7',
    'Die Pfadlängen von k₁ zu allen anderen 14 Knoten ergeben aufsummiert 16. Der Mittelwert ist 16/14 = 16/7.'
)
""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("✅ Tabelle edge_small_questions erfolgreich erstellt und Beispiel-Frage eingefügt.")
