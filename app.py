import sys
from flask import Flask, request, jsonify, render_template
from gpt_interface_handler import generate_chat_response, extract_score_from_text, parse_table_ratings
import openai
import os
import time
import json
import re
import random
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = True

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = "asst_kcgKTBiEYbVcvgwjSxl6yCVm"

# Verbindung zu Neon PostgreSQL
DB_URL = os.getenv("NEON_DB_URL")

def get_conn():
    return psycopg2.connect(DB_URL)

# ✅ Chatverlauf abrufen
def get_chat_history():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question, user_message, assistant_response FROM chat_history ORDER BY timestamp DESC LIMIT 10")
        history = cursor.fetchall()
    return [{"question": row[0], "user": row[1], "assistant": row[2]} for row in history]



# ✅ Zufällige Frage aus der Datenbank abrufen
import random

# ✅ Abrufen einer zufälligen Tabellenfrage
def get_table_question(question_text):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM table_questions WHERE question = %s", (question_text,))
        result = cursor.fetchone()
        if result:
            question_id = result[0]
            cursor.execute("SELECT topology, cluster_solution, diameter_solution FROM question_table_data WHERE question_id = %s", (question_id,))
            table_data = cursor.fetchall()
            return {
                "question_type": "table",
                "question": question_text,
                "table_data": [{"topology": row[0], "cluster": row[1], "diameter": row[2]} for row in table_data]
            }
    return {"error": "Keine Tabellenfrage gefunden!"}


def get_single_question_by_text(question_text):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question, ideal_answer FROM single_questions WHERE question = %s", (question_text,))
        row = cursor.fetchone()
    if row:
        return {"question": row[0], "ideal_answer": row[1]}
    return None


def get_image_question():
    with get_conn() as conn:
        print("🔍 TEST: `get_next_question()` wurde aufgerufen!")  # Debugging
        cursor = conn.cursor()
        cursor.execute("SELECT question, ideal_answer, image_path FROM image_questions ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
    if row:
        return {"question": row[0], "ideal_answer": row[1], "image_path": row[2]}
    return None


def get_gefangenendilemma_a_by_kombination(kombinationen):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT kombination, a_wert, b_wert, gesamt FROM gefangenendilemma_a WHERE kombination = ANY(%s)",
            (kombinationen,)
        )
        rows = cursor.fetchall()
    return {row[0]: [row[1], row[2], row[3]] for row in rows}


def get_gefangenendilemma_b_question_by_text(question_text):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, ideal_strategy_a, ideal_strategy_b, total_score_a, total_score_b
            FROM gefangenendilemma_b
            WHERE question = %s
        """, (question_text,))
        row = cursor.fetchone()
    if row:

        return {
            "question": row[0],
            "ideal_strategy_a": json.loads(row[1]) if isinstance(row[1], str) else row[1],
            "ideal_strategy_b": json.loads(row[2]) if isinstance(row[2], str) else row[2],
            "total_score_a": row[3],
            "total_score_b": row[4]
        }

    return None




def get_parallelitaetabc_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, step1_prompt, step1_ideal, step2_prompt, step2_ideal,
                   step3_prompt, step3_ideal, step4_prompt, step4_ideal
            FROM parallelitaetabc_questions
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return {
                "question": row[0],
                "step1_prompt": row[1],
                "step1_ideal": row[2],
                "step2_prompt": row[3],
                "step2_ideal": row[4],
                "step3_prompt": row[5],
                "step3_ideal": row[6],
                "step4_prompt": row[7],
                "step4_ideal": row[8],
            }
        return None




def get_edge_small_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM edge_small_questions ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {
                "question": row[1],
                "sub_a": row[2],
                "solution_a": row[3],
                "explanation_a": row[4],
                "sub_b": row[5],
                "solution_b": row[6],
                "explanation_b": row[7]
            }
        return None


def get_edge_small2_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM edge_small_questions2 ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {
                "question": row[1],
                "sub_a_label": row[2],
                "sub_b_label": row[3],
                "sub_c_label": row[4],
                "ideal_a": row[5],
                "ideal_b": row[6],
                "ideal_c": row[7]
            }
        return None


def get_hubauths1_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hubauths1 ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        print("📦 Ergebnis aus hubauths1:", row)  # 👈 NEU
        if row:
            return {
                "question_type": "hubauths1",
                "question": row[2],
                "image_path": row[1],
                "subquestion1": row[2],
                "adj_matrix": row[3],
                "subquestion2": row[4],
                "eigenvalue": row[5],
                "eigenvalue_explanation": row[6],
                "hub_vector": [row[7], row[8], row[9]],
                "hub_explanation": row[10],
                "authority_vector": [row[11], row[12], row[13]],
                "authority_explanation": row[14]
            }
        return None


def get_signalklassi_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, input1, input2, input3, input4, input5, input6, input7,
                    image1, image2, image3, image4, image5
            FROM signalklassi_questions
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return {
                "question": row[0],
                "ideal_answers": list(row[1:8]),
                "image_paths": list(row[8:13])
            }
        return None


def get_fourier_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, image_path, hint, tip,
                   a0_answer, a0_explanation,
                   ak_answer, ak_explanation,
                   bk_answer, bk_explanation
            FROM fourier_questions
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return {
                "question": row[0],
                "image_path": row[1],
                "hint": row[2],
                "tip": row[3],
                "ideal_answers": {
                    "a0": row[4],
                    "a0_expl": row[5],
                    "ak": row[6],
                    "ak_expl": row[7],
                    "bk": row[8],
                    "bk_expl": row[9]
                }
            }
        return None

def get_abtastung_question():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT intro, teil1_prompt, teil2_prompt, teil1_answer, teil1_unit, teil1_explanation, teil2_answer, teil2_unit, teil2_explanation
            FROM abtastung_questions
            ORDER BY RANDOM()
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return {
                "intro": row[0],
                "teil1_prompt": row[1],
                "teil2_prompt": row[2],
                "solution_fa": row[3],
                "solution_fa_unit": row[4],
                "solution_expl1": row[5],
                "solution_fr": row[6],
                "solution_fr_unit": row[7],
                "solution_expl2": row[8],
                "ideal_answers": {
                    "teil1_answer": row[3],
                    "teil1_unit": row[4],
                    "teil1_expl": row[5],
                    "teil2_answer": row[6],
                    "teil2_unit": row[7],
                    "teil2_expl": row[8]
                }
            }
        return None



# ✅ Hauptseite rendern
@app.route("/")
def index():
    print("🚀 Flask lädt die HTML-Seite: index.html", flush=True)  # Debugging-Print
    return render_template("index.html")

import re  # Falls noch nicht importiert


def extract_score_from_text(gpt_answer):
    match = re.search(r'(?:Bewertung:\s*|^)(\d+)[\.\s]', gpt_answer)
    if match:
        return int(match.group(1))
    return None


####################################################################################################################################


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()
    print("📨 Empfange Daten:", data)

    if not data or "question_type" not in data or "user_inputs" not in data:
        print("❌ Ungültige Anfrage:", data)
        return jsonify({"error": "Ungültige Anfrage"}), 400

    #question_type = data.get("question_type", "").strip()
    question_type = data.get("question_type", "").strip().lower()

    user_inputs = data.get("user_inputs", {})

    question = data.get("question", "").strip()


    # Hole Musterlösung aus deiner Datenbank (je nach Fragetyp)
    if question_type == "gefangenendilemma_b":
        solution_data = get_gefangenendilemma_b_question_by_text(question)
    elif question_type == "gefangenendilemma_a":
        kombinationen = list(user_inputs.keys())
        solution_data = get_gefangenendilemma_a_by_kombination(kombinationen)
    elif question_type == "table":
        solution_data = get_table_question(question)
    elif question_type == "single_questions":
        solution_data = get_single_question_by_text(question)
    elif question_type == "image":
        solution_data = get_image_question()
    elif question_type == "parallelitaetabc":
        solution_data = get_parallelitaetabc_question()
    elif question_type == "ea2_edgesmall_a1a2":
        solution_data = get_edge_small_question()
    elif question_type == "ea2_edgesmall_a3":
        solution_data = get_edge_small2_question()
    elif question_type == "hubauths1":
        solution_data = get_hubauths1_question()
    elif question_type == "signalklassi":
        solution_data = get_signalklassi_question()
    elif question_type == "fourier":
        solution_data = get_fourier_question()
    elif question_type == "abtastung":
        solution_data = get_abtastung_question()
    else:
        return jsonify({"error": f"Unbekannter Fragetyp: {question_type}"}), 400

    # Validierung
    if not question or not user_inputs:
        print("❌ Frage oder Eingaben leer:", question, user_inputs)
        return jsonify({"error": "Leere Eingabe"}), 400

    # Debug-Ausgabe der geladenen Daten
    print("📦 Prüfe solution_data... (aktueller Fragetyp:", question_type, ")")
    print("↪️ Aktuelle Lösung:", solution_data)

    if not solution_data:
        print("❌ Keine Musterlösung gefunden!")
        return jsonify({"error": "Keine Musterlösung gefunden"}), 404

    print("📩 Debug Backend:")
    print("- Fragetyp:", question_type)
    print("- Frage:", question)
    print("- Eingaben:", user_inputs)
    print("- Musterlösung:", solution_data)

    try:
        score, gpt_answer = generate_chat_response(question_type, question, user_inputs, solution_data)
    except Exception as e:
        print("❌ Fehler in generate_chat_response:", e)
        return jsonify({"error": "Fehler bei generate_chat_response", "details": str(e)}), 500

    print("- GPT-Antwort:", gpt_answer)
    print("- GPT-Score:", score)

    if not gpt_answer:
        return jsonify({"error": "Keine GPT-Antwort erhalten"}), 500


    if question_type == "table":
        table_ratings = parse_table_ratings(gpt_answer, user_inputs)

        gpt_response = {
            "rating": table_ratings,
            "summary": "Vergleich abgeschlossen. Detaillierte Bewertungen siehe oben."
        }

        print("⚠️ Konnte GPT-Antwort nicht als JSON parsen.")

        gpt_response = {
            "rating": table_ratings,
            "summary": "Vergleich abgeschlossen. Detaillierte Bewertungen siehe oben."
        }


    elif question_type == "gefangenendilemma_a":
        gpt_response = {}
        for key in ["R", "S", "T", "P"]:
            match = re.search(rf'{key}:\s*(\d+)', gpt_answer)
            gpt_response[key] = {
                "score": int(match.group(1)) if match else 0,
                "comment": "Siehe GPT-Antwort für Details."
        }


    elif question_type == "gefangenendilemma_b":
        gpt_response = gpt_answer  # gpt_answer ist bereits das vollständige dict mit A/B-Bewertung


    elif question_type == "ea2_edgesmall_a1a2":
        # Bewertung parsen
        pattern = r"(a|b)\)\s*Antwort:\s*(\d)\s*[–-]\s*(.+)"
        matches = re.findall(pattern, gpt_answer)

        gpt_response = {}
        for teil, score, comment in matches:
            gpt_response[teil] = {
                "score": int(score),
                "comment": comment.strip()
            }

        if not gpt_response:
            gpt_response = {
                "score": 0,
                "comment": "⚠️ Keine verwertbare GPT-Antwort erhalten."
            }

    elif question_type == "ea2_edgesmall_a3":
        pattern = r"(a|b|c)\)\s*Antwort:\s*(\d)\s*[–-]\s*(.+)"
        matches = re.findall(pattern, gpt_answer)

        gpt_response = {}
        for teil, score, comment in matches:
            gpt_response[teil] = {
                "score": int(score),
                "comment": comment.strip()
            }

        if not gpt_response:
            gpt_response = {
                "score": 0,
                "comment": "⚠️ Keine verwertbare GPT-Antwort erhalten."
            }


    elif question_type == "hubauths1":
        solution_data = get_hubauths1_question()
        question = (
                solution_data.get("subquestion1", "").strip()
                + "\n\n" +
                solution_data.get("subquestion2", "").strip()
        )
        # 🔒 Pflichtfelder nur hier prüfen
        required_fields = [
            "adj_matrix", "eigenvalue", "eigenvalue_explanation",
            "hub_vector", "hub_explanation",
            "authority_vector", "authority_explanation"
        ]

        for field in required_fields:
            value = user_inputs.get(field)

            # Leere Strings, Arrays oder nur Whitespace abfangen
            if value is None or (isinstance(value, str) and not value.strip()) or (
                    isinstance(value, list) and all(not v.strip() for v in value if isinstance(v, str))):
                print("❌ Fehlendes oder leeres Feld:", field)
                return jsonify({"error": f"Leere Eingabe bei {field}"}), 400

        print("🔍 Bearbeite Fragetyp: hubauths1")
        print("➡️ Frage:", question)
        print("➡️ Eingaben:", user_inputs)
        print("➡️ Musterlösung:", solution_data)

        # 🔢 Automatische Bewertung der Adjazenzmatrix (0.5 Punkte pro richtigem Eintrag)
        ideal_matrix = solution_data.get("adj_matrix", "")
        user_matrix = user_inputs.get("adj_matrix", "")

        ideal_flat = [entry.strip() for row in ideal_matrix.split(";") for entry in row.strip().split(",")]
        user_flat = [entry.strip() for row in user_matrix.split(";") for entry in row.strip().split(",")]

        print("✅ Ideal Flat:", ideal_flat)
        print("✅ User Flat:", user_flat)

        correct_count = sum(1 for u, i in zip(user_flat, ideal_flat) if u == i)
        matrix_score = correct_count * 0.5

        # 🧠 GPT-Response direkt mit Matrix starten
        gpt_response = {
            "Matrix": {
                "score": matrix_score,
                "comment": f"Die Adjazenzmatrix hat {correct_count} von {len(ideal_flat)} Einträgen korrekt. Eingabe: {user_matrix} | Musterlösung: {ideal_matrix}"
            }
        }
        gesamtpunktzahl = matrix_score

        # GPT-Antworten parsen (m, h, a)
        pattern = r"(m|h|a)\s*[:\-]\s*(\d+(?:[.,]\d+)?)\s*[–-]\s*(.+)"
        matches = re.findall(pattern, gpt_answer)

        for teil, score, comment in matches:
            label = teil.strip()
            score_float = float(score.replace(",", "."))  # Kommas erlauben
            gpt_response[label] = {
                "score": score_float,
                "comment": comment.strip()
            }
            gesamtpunktzahl += score_float

        # Gesamtbewertung ergänzen
        gpt_response["total_score"] = {
            "score": gesamtpunktzahl,
            "comment": f"Gesamtpunktzahl: {gesamtpunktzahl:.1f} / 19.5"
        }

        # Notfall-Fallback, falls alles schiefläuft
        if not gpt_response:
            gpt_response = {
                "score": 0,
                "comment": "⚠️ Keine verwertbare GPT-Antwort erhalten."
            }






    elif question_type == "signalklassi":
        print("📥 GPT-Antwort (raw):", gpt_answer)  # 👈 Debug-Print hier einfügen
        # Antworten für 7 Felder extrahieren
        pattern = r"Eingabe\s*(\d+):\s*([0-5])\s*[–-]\s*(.+)"
        matches = re.findall(pattern, gpt_answer)

        gpt_response = {}
        for number, score, comment in matches:
            gpt_response[f"Eingabe {number}"] = {
                "score": float(score) * 0.1,
                "comment": comment.strip()
            }

        if not gpt_response:
            gpt_response = {
                "score": 0,
                "comment": "⚠️ Keine verwertbare GPT-Antwort erhalten."
            }

    elif question_type == "parallelitaetabc":

        pattern = r"Schritt\s*(\d):\s*([0-2])\s*[–\-]\s*(.+?)(?=\nSchritt\s*\d:|\Z)"
        matches = re.findall(pattern, gpt_answer, re.DOTALL)

        gpt_response = {}
        for step, score, comment in matches:
            gpt_response[f"Schritt {step}"] = {
                "score": int(score),
                "comment": comment.strip()
            }

        if not gpt_response:
            gpt_response = {
                "score": 0,
                "comment": "⚠️ Keine verwertbare GPT-Antwort erhalten."
            }




    elif question_type == "fourier":
        pattern = r"(Antwort|Begründung)\s+(a₀/2|aₖ|bₖ):\s*([0-5])\s*[–-]\s*(.+)"
        matches = re.findall(pattern, gpt_answer)

        gpt_response = {}
        for typ, name, score, comment in matches:
            label = f"{typ} {name}"
            gpt_response[label] = {
                "score": int(score),
                "comment": comment.strip()
            }

    elif question_type == "abtastung":
        pattern = r"Teil\s*(\d+)\s*[–-]\s*(Antwort|Begründung):\s*([0-5])\s*[–-]\s*(.+)"
        matches = re.findall(pattern, gpt_answer)

        gpt_response = {}
        for teil, typ, score, comment in matches:
            label = f"Teil {teil} – {typ}"
            gpt_response[label] = {
                "score": int(score),
                "comment": comment.strip()
            }

        if not gpt_response:
            gpt_response = {
                "score": 0,
                "comment": "⚠️ Keine verwertbare GPT-Antwort erhalten."
            }


    else:
        gpt_response = {
            "score": score if score is not None else 0,
            "comment": gpt_answer
        }

    # Bewertung speichern (optional)
    with get_conn() as conn:
        cursor = conn.cursor()
        rating_value = json.dumps(gpt_response["rating"]) if question_type == "table" else gpt_response.get("score", 0)
        cursor.execute("""
            INSERT INTO chat_history (question, user_message, assistant_response, rating)
            VALUES (%s, %s, %s, %s)
        """, (question, json.dumps(user_inputs), json.dumps(gpt_response), rating_value))
        conn.commit()

    return jsonify({
        "message": "Erfolg!",
        "gpt_response": gpt_response,
        **solution_data  # ⬅️ fügt alle Musterlösungsfelder mit in die JSON-Antwort ein
    }), 200


################################################################################################################################################






@app.route("/next-question", methods=["GET"])
def next_question():
    print("🔍 `next_question` wurde aufgerufen!")


    # Falls expliziter Typ übergeben wurde (z. B. /next-question?type=fourier), nimm diesen
    requested_type = request.args.get("type")
    question_type = requested_type if requested_type else random.choice([
        "table", "single_questions", "gefangenendilemma_a", "gefangenendilemma_b",
        "parallelitaetabc", "EA2_EdgeSmall_A1A2", "EA2_EdgeSmall_A3", "hubauths1",
        "signalklassi", "fourier", "abtastung"
    ])

    with get_conn() as conn:
        cursor = conn.cursor()
        result = None

        if question_type == "table":
            cursor.execute("SELECT id, question FROM table_questions ORDER BY RANDOM() LIMIT 1")
            result = cursor.fetchone()
            if result:
                question_id, question_text = result
                print(f"✅ Tabellenfrage gefunden: {question_text} (ID: {question_id})")
                cursor.execute("SELECT topology, cluster_solution, diameter_solution FROM question_table_data WHERE question_id = %s", (question_id,))
                table_data = cursor.fetchall()
                return jsonify({
                    "question_type": "table",
                    "question": question_text,
                    "table_data": [{"topology": row[0], "cluster": row[1], "diameter": row[2]} for row in table_data]
                })


        elif question_type == "single_questions":  # <- korrekt mit 's'
            print("📌 single_questions ausgewählt")
            cursor.execute("SELECT * FROM single_questions ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "single_questions",
                    "question": row[1],
                    "ideal_answer": row[2]
                })


        elif question_type == "image":
            cursor.execute("SELECT question, ideal_answer, image_path FROM image_questions ORDER BY RANDOM() LIMIT 1")
            result = cursor.fetchone()
            if result:
                print(f"📷 Bildfrage gefunden: {result[0]} (Bild: {result[2]})")
                return jsonify({
                    "question_type": "image",
                    "question": result[0],
                    "ideal_answer": result[1],
                    "image_path": result[2]
                })

        elif question_type == "gefangenendilemma_a":
            print("🎯 Gefangenendilemma A ausgewählt")
            cursor.execute("SELECT * FROM gefangenendilemma_a")
            rows = cursor.fetchall()
            if rows:
                return jsonify({
                    "question_type": "gefangenendilemma_a",
                    "question": "Füllen Sie die Matrix zum Gefangenendilemma aus (Abschnitt a).",
                    "table_data": [
                        {"kombination": row[1], "a": row[2], "b": row[3], "gesamt": row[4]} for row in rows
                    ]
                })

        elif question_type == "gefangenendilemma_b":
            print("🎯 Gefangenendilemma B ausgewählt")
            cursor.execute("SELECT question, ideal_strategy_a, ideal_strategy_b FROM gefangenendilemma_b ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            print("👀 Typ von ideal_strategy_a:", type(row[1]))
            print("👀 Inhalt von ideal_strategy_a:", row[1])
            if row:
                return jsonify({
                    "question_type": "gefangenendilemma_b",
                    "question": row[0],
                    "ideal_a": row[1],
                    "ideal_b": row[2]
                })

        elif question_type == "parallelitaetabc":
            print("🎯 parallelitaetabc ausgewählt")
            cursor.execute("""
                SELECT question, step1_prompt, step2_prompt, step3_prompt, step4_prompt,
                       step1_ideal, step2_ideal, step3_ideal, step4_ideal
                FROM parallelitaetabc_questions
                ORDER BY RANDOM() LIMIT 1
            """)

            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "parallelitaetabc",
                    "question": row[0],
                    "step1_prompt": row[1],
                    "step2_prompt": row[2],
                    "step3_prompt": row[3],
                    "step4_prompt": row[4],
                    "ideal_answers": [row[5], row[6], row[7], row[8]]
                    })

        elif question_type == "EA2_EdgeSmall_A1A2":
            print("📌 EA2_EdgeSmall_A1A2 ausgewählt")
            cursor.execute("SELECT * FROM edge_small_questions ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "EA2_EdgeSmall_A1A2",
                    "question": row[1],
                    "subquestion_a": row[2],
                    "solution_a": row[3],
                    "explanation_a": row[4],
                    "subquestion_b": row[5],
                    "solution_b": row[6],
                    "explanation_b": row[7]
                    })

        elif question_type == "EA2_EdgeSmall_A3":
            print("📌 EA2_EdgeSmall_A3 ausgewählt")
            cursor.execute("SELECT * FROM edge_small_questions2 ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "EA2_EdgeSmall_A3",
                    "question": row[1],
                    "sub_a_label": row[2],
                    "sub_b_label": row[3],
                    "sub_c_label": row[4],
                    "solution_a": row[5],
                    "solution_b": row[6],
                    "solution_c": row[7]
                })


        elif question_type == "hubauths1":
            print("📌 HubAuths1 ausgewählt")
            cursor.execute("SELECT * FROM hubauths1 ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "hubauths1",
                    "question": row[2],
                    "image_path": row[1],
                    "subquestion1": row[2],
                    "adj_matrix": row[3],
                    "subquestion2": row[4],
                    "eigenvalue": row[5],
                    "eigenvalue_explanation": row[6],
                    "hub_vector": [row[7], row[8], row[9]],
                    "hub_explanation": row[10],
                    "authority_vector": [row[11], row[12], row[13]],
                    "authority_explanation": row[14]
                })



        elif question_type == "signalklassi":
            print("📌 Signalklassi-Fragetyp ausgewählt")
            cursor.execute("""
                SELECT question, input1, input2, input3, input4, input5, input6, input7,
                       image1, image2, image3, image4, image5
                FROM signalklassi_questions
                ORDER BY RANDOM()
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "signalklassi",
                    "question": row[0],
                    "ideal_answers": list(row[1:8]),  # input1–input7
                    "image_paths": list(row[8:13])  # image1–image5
                })

        elif question_type == "fourier":
            print("📌 Fourier-Aufgabe ausgewählt")
            cursor.execute("SELECT * FROM fourier_questions ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "fourier",
                    "question": row[1],
                    "image_path": row[2],
                    "hint": row[3],
                    "tip": row[4],
                    "ideal_answers": {
                        "a0": row[5],
                        "a0_expl": row[6],
                        "ak": row[7],
                        "ak_expl": row[8],
                        "bk": row[9],
                        "bk_expl": row[10]
                    }
                })



        elif question_type == "abtastung":
            print("📌 Abtastung-Frage ausgewählt")
            cursor.execute("SELECT * FROM abtastung_questions ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({
                    "question_type": "abtastung",
                    "intro": row[1],
                    "teil1_prompt": row[2],
                    "teil2_prompt": row[3],
                    "solution_fa": row[4],
                    "solution_fa_unit": row[5],
                    "solution_expl1": row[6],
                    "solution_fr": row[7],
                    "solution_fr_unit": row[8],
                    "solution_expl2": row[9]
                })

    print("❌ Keine Fragen gefunden!")
    return jsonify({"error": "Keine Fragen gefunden!"}), 404



# ✅ FLask-Server-Start
if __name__ == "__main__":
    print("\n📌 Registrierte Routen:")
    print(app.url_map)  # Debugging: Alle Flask-Routen anzeigen

    app.run(debug=True)
