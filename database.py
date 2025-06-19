
import psycopg2
import os
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Tabellen erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS single_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    ideal_answer TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS table_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS question_table_data (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    topology TEXT NOT NULL,
    cluster_solution TEXT NOT NULL,
    diameter_solution TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES table_questions(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS image_questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    ideal_answer TEXT NOT NULL,
    image_path TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gefangenendilemma_a (
    id SERIAL PRIMARY KEY,
    kombination TEXT NOT NULL,
    a_wert TEXT NOT NULL,
    b_wert TEXT NOT NULL,
    gesamt TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gefangenendilemma_b (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    ideal_strategy_a TEXT[] NOT NULL,
    ideal_strategy_b TEXT[] NOT NULL,
    total_score_a INTEGER NOT NULL,
    total_score_b INTEGER NOT NULL
)
""")

# Beispiel-Daten einfügen

# single_questions (3 Einträge)
single_questions_data = [
    ("Erkläre den Unterschied zwischen künstlicher Intelligenz und maschinellem Lernen.",
     "Künstliche Intelligenz ist das übergeordnete Feld, maschinelles Lernen ist eine Teilmenge davon, die auf Daten basiert."),
    ("Was sind die besten Sicherheitspraktiken für Web-Development?",
     "Eingabevalidierung, HTTPS-Verschlüsselung, sichere Passwortspeicherung, regelmäßige Updates und Zugriffskontrolle sind essenziell."),
    ("Im Kurs haben Sie einige Beispiel für Strukturen in Natur und Technik kennengelernt. Nennen Sie fünf weitere Beispiel für Strukturen aus diesen Bereichen:",
     "• Das Stromnetz\n• Drahtgebundenes Telekommunikationsnetz\n• Ausbreitung ansteckender Krankheiten\n• Sanddünen in der Wüste\n• Vogel- und Fischschwärme\n• Hierarchien in Organisationen oder anderen sozialen Gemeinschaften auch bei Tieren")
]
cursor.executemany("INSERT INTO single_questions (question, ideal_answer) VALUES (%s, %s)", single_questions_data)

# Frage für Tabellenaufgabe
cursor.execute("INSERT INTO table_questions (question) VALUES (%s) RETURNING id",
               ("Bestimmen Sie die Kennzahlen für folgende Topologien:",))
table_question_id = cursor.fetchone()[0]

# Acht vollständige Einträge
table_data = [
    (table_question_id, "Quadratisches Gitter mit Knotenzahl n²", "Kein Nachbar ist direkt mit einem anderen Nachbarn vernetzt. Der globale Clusterkoeffizient hat den Wert 0.", "Abstand zweier gegenüberliegender Ecken (Manhattan-Metrik): 2(n−1)"),
    (table_question_id, "Bus mit n Stationen", "Hier kann man streiten. [...] Clusterkoeffizient ist also 1.", "Es greift dieselbe Argumentation. [...] Durchmesser ist also 1."),
    (table_question_id, "Ring mit n Stationen", "Kein Nachbar eines Knotens ist direkt mit einem anderen Nachbarn desselben Knotens vernetzt. Der Clusterkoeffizient ist 0.", "Die größte Distanz tritt zwischen zwei gegenüberliegenden Knoten auf. Der Durchmesser beträgt n/2."),
    (table_question_id, "Ring mit n Stationen und unidirektionalen Verweisen", "Hier ändert sich nichts, der Clusterkoeffizient ist 0.", "Es gibt nur noch eine Richtung durch den Graphen. Jeder Knoten hat zu dem Nachbarn, mit dem er nicht gerichtet verbunden ist, die Distanz von n-1."),
    (table_question_id, "Stern mit n Stationen", "* In der Sternstruktur haben nicht alle Knoten denselben lokalen Clusterkoeffizienten. [...] globale Clusterkoeffizient den Wert 0 hat.", "Um zwei Randknoten zu verbinden, muss stets durch den Zentrumsknoten vermittelt werden, der Durchmesser ist 2."),
    (table_question_id, "d-dimensionaler Hyperwürfel", "Kein Nachbar eines Knotens ist direkt mit einem anderen Nachbarn desselben Knotens vernetzt. Der Clusterkoeffizient ist 0.", "Per Definition des Hyperwürfels: d. In jeder Dimension ist nur ein Vermittlungsschritt notwendig."),
    (table_question_id, "Vollständig vermaschtes Netz mit n Stationen", "Jeder ist mit jedem vernetzt. Der Clusterkoeffizient hat den Wert 1.", "Jeder ist mit jedem vernetzt. Der Durchmesser ist 1."),
    (table_question_id, "Balancierte k-närer Baum mit n Elementen", "Kein Nachbar eines Knotens ist direkt mit einem anderen Nachbarn desselben Knotens vernetzt. Der Clusterkoeffizient ist 0.", "Per Definition ist die Höhe des k-nären balancierten Baumes maximal c · logₖ n [...] Abstand 2 · c · logₖ n.")
]
cursor.executemany(
    "INSERT INTO question_table_data (question_id, topology, cluster_solution, diameter_solution) VALUES (%s, %s, %s, %s)",
    table_data
)

# Daten für gefangenendilemma_a (12 Zeilen)
dilemma_a = [("R", "3", "3", "6"), ("S", "0", "8", "8"), ("T", "8", "0", "8"), ("P", "1", "1", "2")] * 3
cursor.executemany(
    "INSERT INTO gefangenendilemma_a (kombination, a_wert, b_wert, gesamt) VALUES (%s, %s, %s, %s)", dilemma_a)

# gefangenendilemma_b (2 gleiche Zeilen)
dilemma_b = [(
    "Welche Kooperationsstrategie bringt für A und B jeweils über mehrere Runden hinweg den maximalen Nutzen?",
    ['höre Musik', 'höre Musik', 'ist still', 'ist still'],
    ['höre Musik', 'ist still', 'höre Musik', 'ist still'],
    14, 12
)] * 2
cursor.executemany(
    "INSERT INTO gefangenendilemma_b (question, ideal_strategy_a, ideal_strategy_b, total_score_a, total_score_b) VALUES (%s, %s, %s, %s, %s)",
    dilemma_b
)

conn.commit()
conn.close()
print("✅ Datenbankstruktur aktualisiert und Daten eingesetzt.")