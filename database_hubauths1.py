import psycopg2
import os
from dotenv import load_dotenv

# .env-Datei laden für DB-Verbindung
load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")

# Verbindung herstellen
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Tabelle für HubAuths1-Fragetyp erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS hubauths1 (
    id SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL,
    subquestion1 TEXT NOT NULL,
    adj_matrix TEXT NOT NULL,
    subquestion2 TEXT NOT NULL,
    eigenvalue TEXT NOT NULL,
    eigenvalue_explanation TEXT NOT NULL,
    hub_vector_1 TEXT NOT NULL,
    hub_vector_2 TEXT NOT NULL,
    hub_vector_3 TEXT NOT NULL,
    hub_explanation TEXT NOT NULL,
    auth_vector_1 TEXT NOT NULL,
    auth_vector_2 TEXT NOT NULL,
    auth_vector_3 TEXT NOT NULL,
    auth_explanation TEXT NOT NULL
)
""")

# Beispiel-Datensatz einfügen
cursor.execute("""
INSERT INTO hubauths1 (
    image_path,
    subquestion1,
    adj_matrix,
    subquestion2,
    eigenvalue,
    eigenvalue_explanation,
    hub_vector_1,
    hub_vector_2,
    hub_vector_3,
    hub_explanation,
    auth_vector_1,
    auth_vector_2,
    auth_vector_3,
    auth_explanation
) VALUES (
    'images/image.png',
    'Bestimmen Sie die Adjazenzmatrix.',
    '0,1,0;1,0,1;1,0,0',
    'Bestimmen Sie die Hub- und Authority-Vektoren h und a für die Knoten des Graphen, indem Sie das nachfolgende Eigenvektor-Problem lösen:\\n\\n$$ A \\cdot A^T \\cdot h = m \\cdot h $$\\n\\n$$ A^T \\cdot A \\cdot a = m \\cdot a $$\\n\\nHinweis: Für den Algorithmus ist nur der Eigenvektor zum betragsmäßig größten Eigenwert m zu betrachten.',
    '3',
    'In dem gegebenen Graphen existieren die gerichteten Kanten 1 → 2, 2 → 1, 2 → 3 und 3 → 1.\\nDaraus ergibt sich die Adjazenzmatrix A und ihre Transponierte A^T:\\n$$ A= \\begin{pmatrix} 0 & 1 & 0\\\\ 1 & 0 & 1\\\\ 1 & 0 & 0 \\end{pmatrix} $$, $$ A^T= \\begin{pmatrix} 0 & 1 & 1\\\\ 1 & 0 & 0\\\\ 0 & 1 & 0 \\end{pmatrix} $$\\nDas charakteristische Polynom ist $$P(m)= -m^3 + 4m^2 -4m +1$$ mit Eigenwerten ca. 0,38; 1; 2,62',
    '0',
    '1.62',
    '1',
    'Der betragsmäßig größte Eigenwert ist $$ m_3 $$, sodass der Hubvektor durch \\n$$ (A \\cdot A^T - m_3 E) \\cdot \\vec{h} = 0 $$ bestimmt wird. Lösung: $$ \\vec{h}=\\begin{pmatrix} 0\\\\ 1.62\\\\ 1 \\end{pmatrix} $$',
    '1.62',
    '0',
    '1',
    'Analoges Eigenwertproblem für $$ A^T \\cdot A $$ mit identischem größtem Eigenwert.\\nAuthorityvektor: $$ \\vec{a}=\\begin{pmatrix} 1.62\\\\ 0\\\\ 1 \\end{pmatrix} $$'
)
""")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("✅ Tabelle hubauths1 erfolgreich erstellt und Beispiel-Frage eingefügt.")
