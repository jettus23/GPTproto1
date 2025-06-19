import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Neue Tabelle erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS edge_small_questions2 (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    sub_a_label TEXT NOT NULL,
    sub_b_label TEXT NOT NULL,
    sub_c_label TEXT NOT NULL,
    ideal_a TEXT NOT NULL,
    ideal_b TEXT NOT NULL,
    ideal_c TEXT NOT NULL
)
""")

# Beispielaufgabe einfügen
cursor.execute("""
INSERT INTO edge_small_questions2 (
    question, sub_a_label, sub_b_label, sub_c_label,
    ideal_a, ideal_b, ideal_c
) VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (
    """Gegeben sei ein Ring mit N=15 Knoten k₁, k₂, ..., k₁₅ und d=4. D.h. jeder Knoten ist nicht nur 
    mit seinen direkten Nachbarn, sondern auch mit seinen jeweils übernächsten Nachbarn in beide Richtungen verbunden.

Biegen Sie nun gedanklich nach dem Modell von Watts & Strogatz die Verbindung von k₁ zu k₃ so um, dass k₁ nun mit k₈ verbunden ist (und demnach nicht mehr direkt mit k₃).
Bestimmen Sie erneut die mittlere Pfadlänge von k₁ zu den anderen Knoten und vergleichen Sie diesen Wert mit dem Ergebnis der vorherigen Aufgabe.""",
    "Neue mittlere Pfadlänge:",
    "Rechenweg",
    "Vergleich zu Teil 2",
    "13/7",
    "(1+1+2+2+3+2+2+1+2+2+3+2+2+1)/14 = 13/7",
    "Das Edge Reassignment an Knoten 1 verkürzt also die durchschnittliche Pfadlänge von k₁ zu den anderen Knoten um 3/16 = 18,75%."
))


conn.commit()
conn.close()

print("✅ Tabelle edge_small_questions2 erfolgreich erstellt und befüllt.")
