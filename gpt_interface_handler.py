import os
import time
import json
import re
import openai
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = "asst_kcgKTBiEYbVcvgwjSxl6yCVm"

def extract_score_from_text(gpt_answer):
    match = re.search(r'(?:Bewertung:\s*|^)(\d+)[\.\s]', gpt_answer)
    if match:
        return int(match.group(1))
    return None


def parse_table_ratings(gpt_answer, user_inputs):
    entries = gpt_answer.strip().split('---')
    ratings = []
    for entry in entries:
        topology_match = re.search(r'Topologie:\s*(.+)', entry)
        score_match = re.search(r'Bewertung:\s*(\d+)', entry)
        comment_match = re.search(r'Kommentar:\s*(.+)', entry, re.DOTALL)
        if topology_match and score_match and comment_match:
            ratings.append({
                "topology": topology_match.group(1).strip(),
                "score": int(score_match.group(1)),
                "comment": comment_match.group(1).strip()
            })
    return ratings


def generate_chat_response(question_type, question, user_inputs, solution_data):

    if question_type == "table":
        message_content = f"""
        Du erhältst eine Liste von Topologien mit der jeweiligen Musterlösung (Clusterkoeffizient und Durchmesser)  
        und die vom Nutzer eingegebenen Werten.
        
        **Hinweise:**
        - Wenn die Eingabe sprachlich korrekt, aber äquivalent zur Musterlösung ist, bewerte sie trotzdem mit 5/5.
        - Akzeptiere auch erklärende oder alternative Formulierungen, wenn sie mathematisch oder inhaltlich gleichwertig sind.

        
        Musterlösung:
        {json.dumps(solution_data["table_data"], ensure_ascii=False, indent=2)}

        Nutzerantwort:
        {json.dumps(user_inputs, ensure_ascii=False, indent=2)}

        **Deine Aufgabe:**  
        - Gehe jede Topologie einzeln durch.  
        - Vergleiche Clusterkoeffizient und Durchmesser mit der Musterlösung.  
        - Gib folgendes aus:
           ---
           Topologie: <Name>  
           Bewertung: <0-5>  
           Kommentar: <Begründung>
           ---
        """

    elif question_type == "single_questions":
        evaluation_instructions = """
    **Bewertungshinweise für offene Fragen:**

    - Bewerte die Antwort auf einer Skala von 0 bis 5.
    - **0 Punkte** = keine Antwort oder völlig falsche Inhalte.
    - **5 Punkte** = inhaltlich korrekt, vollständig (z. B. alle geforderten Beispiele) und gut formuliert.

    **Kriterien:**
    - Fachliche Richtigkeit der Inhalte
    - Direkter Bezug zur gestellten Frage
    - Auch Beispiele, die im Kurs oder in der Musterlösung genannt wurden, sind gültig und sollen voll gewertet werden.
    - Es wird **nicht verlangt**, dass neue oder originelle Beispiele genannt werden.
    - Die Anzahl der korrekten und thematisch passenden Beispiele kann zur Orientierung der Punktzahl dienen (z. B. 1 Punkt pro gültigem Beispiel).

    **Gib deine Bewertung im folgenden Format zurück:**

    Bewertung: <Zahl zwischen 0 und 5>  
    Kommentar: <Begründung für die Bewertung>

    Beispiel:  
    Bewertung: 3  
    Kommentar: Die Antwort nennt drei gültige Beispiele aus dem Kurs, ist aber sprachlich etwas unklar.
    """

        message_content = f"""
    Frage:
    {question}

    Musterlösung:
    {solution_data.get("ideal_answer", "Nicht verfügbar")}

    Nutzerantwort:
    {user_inputs if isinstance(user_inputs, str) else user_inputs[0]}

    {evaluation_instructions}
    """


    elif question_type == "gefangenendilemma_a":
        def format_values(values):
            return ", ".join(map(str, values)) if isinstance(values, (list, tuple)) else str(values)

        message_content = f"""
        Das Gefangenendilemma (Einzelrunde) wurde beantwortet.

        Nutzerantwort:
        R: {format_values(user_inputs.get("R"))}
        S: {format_values(user_inputs.get("S"))}
        T: {format_values(user_inputs.get("T"))}
        P: {format_values(user_inputs.get("P"))}

        Musterlösung:
        R: {format_values(solution_data.get("R"))}
        S: {format_values(solution_data.get("S"))}
        T: {format_values(solution_data.get("T"))}
        P: {format_values(solution_data.get("P"))}

        **Aufgabe:**
        - Vergleiche jeweils die drei Werte (A, B, Gesamt) für R, S, T und P mit der Musterlösung.
        - Bewerte jeden Block (R/S/T/P) mit 0–3 Punkten.
        - Gib eine Bewertung und eine kurze Begründung je Block.
        Format:
        R: <Bewertung> – <Kommentar>
        ...
        """

    elif question_type == "gefangenendilemma_b":
        print("📥 empfangene user_inputs:", user_inputs)
        user_strategy_a = user_inputs.get("A", [])
        print("🎧 Strategie A (user):", user_strategy_a)
        user_strategy_b = user_inputs.get("B", [])
        print("🎧 Strategie B (user):", user_strategy_b)

        def to_int_safe(value):
            try:
                return int(str(value).strip())
            except (ValueError, TypeError):
                return 0

        a_sum = to_int_safe(user_inputs.get("A_sum"))
        b_sum = to_int_safe(user_inputs.get("B_sum"))

        ideal_a = solution_data["ideal_strategy_a"]
        ideal_b = solution_data["ideal_strategy_b"]
        ideal_sum_a = to_int_safe(solution_data["total_score_a"])  # 🛠️ Fix: sicherstellen, dass int
        ideal_sum_b = to_int_safe(solution_data["total_score_b"])  # 🛠️ Fix: sicherstellen, dass int

        def score_strategy_match(user, ideal):
            return sum(1 for u, i in zip(user, ideal) if u == i)

        def score_sum_match(user_total, ideal_total):
            if user_total == ideal_total:
                return 2
            elif abs(user_total - ideal_total) == 1:
                return 1
            return 0

        a_strategy_score = score_strategy_match(user_strategy_a, ideal_a)
        b_strategy_score = score_strategy_match(user_strategy_b, ideal_b)
        a_score_score = score_sum_match(a_sum, ideal_sum_a)
        b_score_score = score_sum_match(b_sum, ideal_sum_b)

        total_score = a_strategy_score + b_strategy_score + a_score_score + b_score_score

        gpt_response = {
            "A": {
                "score": a_strategy_score + a_score_score,
                "comment": f"Strategie: {a_strategy_score}/4, Genusspunkte: {a_score_score}/2"
            },
            "B": {
                "score": b_strategy_score + b_score_score,
                "comment": f"Strategie: {b_strategy_score}/4, Genusspunkte: {b_score_score}/2"
            }
        }

        return total_score, gpt_response

    elif question_type == "parallelitaetabc":
        message_content = f"""
    Aufgabe zur Bewertung von vier Antworten zur Parallelität.

    Die vier Teile der Nutzerantwort:
    1. Formel: {user_inputs[0]}
    2. Erklärung der Variablen: {user_inputs[1]}
    3. Zusammenfassung des Amdahlschen Gesetzes: {user_inputs[2]}
    4. Schwächen des Gesetzes: {user_inputs[3]}

    Die jeweiligen Musterlösungen:
    1. {solution_data['step1_ideal']}
    2. {solution_data['step2_ideal']}
    3. {solution_data['step3_ideal']}
    4. {solution_data['step4_ideal']}

    Vergleiche jede Nutzerantwort mit der zugehörigen Musterlösung.
    Bewerte jeden Teil **einzeln** mit **0, 1 oder 2 Punkten**.
    Ergänze **jeweils einen kurzen Kommentar**, warum diese Punktzahl vergeben wurde.

    ⚠️ Gib deine Antwort exakt in diesem Format zurück – ohne zusätzliche Erläuterungen oder Einleitung:

    Schritt 1: <Punkte> – <Kommentar>  
    Schritt 2: <Punkte> – <Kommentar>  
    Schritt 3: <Punkte> – <Kommentar>  
    Schritt 4: <Punkte> – <Kommentar>
    """



    elif question_type.lower() == "ea2_edgesmall_a1a2":
        print("📬 Nutzerantworten (EdgeSmall_A1A2):", user_inputs)
        print("📚 Musterlösung:", solution_data)

        message_content = f"""
        Aufgabe: Edge Reassignment in Small-World-Netzen

        Nutzerantwort:
        a) Antwort: {user_inputs.get("a_answer")}
           Rechenweg: {user_inputs.get("a_explanation")}
        b) Antwort: {user_inputs.get("b_answer")}
           Rechenweg: {user_inputs.get("b_explanation")}

        Musterlösung:
        a) Antwort: {solution_data.get("solution_a")}
           Erklärung: {solution_data.get("explanation_a")}
        b) Antwort: {solution_data.get("solution_b")}
           Erklärung: {solution_data.get("explanation_b")}

        - Vergleiche die Antworten mit der Musterlösung.
        - Gib die Bewertung **exakt** im folgenden Format zurück:

        a) Antwort: <Punkte> – <Kommentar>  
        b) Antwort: <Punkte> – <Kommentar>

        """


    elif question_type == "ea2_edgesmall_a3":
        message_content = f"""
        Aufgabe: Erweiterte Analyse zur Edge-Rekonfiguration

        Nutzerantwort:
        a) Neue mittlere Pfadlänge: {user_inputs.get("a_answer")}
        b) Rechenweg: {user_inputs.get("b_answer")}
        c) Vergleich: {user_inputs.get("c_answer")}

        Musterlösung:
        a) {solution_data.get("ideal_a")}
        b) {solution_data.get("ideal_b")}
        c) {solution_data.get("ideal_c")}

        **Aufgabe:**
        - Vergleiche jede Antwort mit der Musterlösung.
        - Gib eine Bewertung von 0–2 pro Teilaufgabe mit kurzer Begründung.
        - Verwende dieses Format:

        a) Antwort: <Punkte> – <Kommentar>  
        b) Antwort: <Punkte> – <Kommentar>  
        c) Antwort: <Punkte> – <Kommentar>
        """


    elif question_type == "hubauths1":
        message_content = f"""
        Aufgabe: Bewertung von Hubs and Authorities (Gewichtung: 19.5 Punkte gesamt)

        Nutzerantwort:
        Adjazenzmatrix (als 3x3 Matrix mit Semikolon-getrennten Zeilen): {user_inputs.get("adj_matrix")}
        Eigenwert: {user_inputs.get("eigenvalue")}
        Erklärung m: {user_inputs.get("eigenvalue_explanation")}
        Hub-Vektor: {user_inputs.get("hub_vector")}
        Erklärung Hub: {user_inputs.get("hub_explanation")}
        Authority-Vektor: {user_inputs.get("authority_vector")}
        Erklärung Authority: {user_inputs.get("authority_explanation")}

        Musterlösung:
        Adjazenzmatrix (als 3x3 Matrix mit Semikolon-getrennten Zeilen): {solution_data.get("adj_matrix")}
        Eigenwert: {solution_data.get("eigenvalue")}
        Erklärung m: {solution_data.get("eigenvalue_explanation")}
        Hub-Vektor: {solution_data.get("hub_vector")}
        Erklärung Hub: {solution_data.get("hub_explanation")}
        Authority-Vektor: {solution_data.get("authority_vector")}
        Erklärung Authority: {solution_data.get("authority_explanation")}

        Bewertungsrichtlinien:
        1. Vergleiche **jede einzelne Zahl der 3x3-Matrix einzeln**. Die Matrix ist als CSV-artige 3x3-Matrix mit Semikolon-getrennten Zeilen und Komma-getrennten Werten übergeben. 
           Zähle, wie viele Einträge genau übereinstimmen (max. 9). Vergib 0.5 Punkte pro korrektem Eintrag → maximal 4.5 Punkte.
           Beispiel:
             Nutzer: "1,0,1;1,0,1;1,0,0"
             Lösung: "0,1,0;1,0,1;1,0,0"
             → ergibt 6 übereinstimmende Werte → 3.0 Punkte.

        2. Vergleiche den Eigenwert und dessen Rechenweg (maximal 5 Punkte)
        3. Vergleiche Hub-Vektor (3 Werte) und Erklärung (gesamt 5 Punkte)
        4. Vergleiche Authority-Vektor (3 Werte) und Erklärung (gesamt 5 Punkte)

        Gib die Bewertung exakt im folgenden Format zurück:

        Matrix: <Punkte von 0–4.5> – <Kommentar>
        m: <Punkte von 0–5> – <Kommentar>
        h: <Punkte von 0–5> – <Kommentar>
        a: <Punkte von 0–5> – <Kommentar>
        """



    elif question_type == "signalklassi":
        message_content = f"""
        Die folgende Aufgabe betrifft die Klassifikation von Signalformen.

        Nutzerantworten:
        1. {user_inputs[0]}
        2. {user_inputs[1]}
        3. {user_inputs[2]}
        4. {user_inputs[3]}
        5. {user_inputs[4]}
        6. {user_inputs[5]}
        7. {user_inputs[6]}

        Musterlösungen:
        1. {solution_data['ideal_answers'][0]}
        2. {solution_data['ideal_answers'][1]}
        3. {solution_data['ideal_answers'][2]}
        4. {solution_data['ideal_answers'][3]}
        5. {solution_data['ideal_answers'][4]}
        6. {solution_data['ideal_answers'][5]}
        7. {solution_data['ideal_answers'][6]}

        **Aufgabe:**
        - Vergleiche jede Nutzerantwort mit der jeweiligen Musterlösung.
        - Gib für jede Eingabe eine Bewertung von 0 bis 0.5 Punkten.
        - Füge eine kurze Begründung hinzu, warum diese Punktzahl vergeben wurde.

        **Wichtig:**
        Gib bitte die Bewertung für jede Eingabe **exakt in folgendem Format** zurück:

        Eingabe 1: <Punktzahl> – <Kommentar>  
        Eingabe 2: <Punktzahl> – <Kommentar>  
        ...
        Eingabe 7: <Punktzahl> – <Kommentar>

        Beispiel:
        Eingabe 1: 4 – Die Antwort ist fast korrekt, aber nicht präzise formuliert.
        """
        print("📤 Prompt an GPT (signalklassi):\n", message_content)


    elif question_type == "fourier":
        message_content = f"""
        Die folgende Aufgabe betrifft die Fourierreihe einer periodisch fortgesetzten Dreieckfunktion.

        Nutzerantworten:
        a₀/2: {user_inputs[0]}
        Begründung a₀/2: {user_inputs[1]}

        aₖ: {user_inputs[2]}
        Begründung aₖ: {user_inputs[3]}

        bₖ: {user_inputs[4]}
        Begründung bₖ: {user_inputs[5]}

        Musterlösungen:
        a₀/2: {solution_data['ideal_answers']['a0']}
        Begründung a₀/2: {solution_data['ideal_answers']['a0_expl']}

        aₖ: {solution_data['ideal_answers']['ak']}
        Begründung aₖ: {solution_data['ideal_answers']['ak_expl']}

        bₖ: {solution_data['ideal_answers']['bk']}
        Begründung bₖ: {solution_data['ideal_answers']['bk_expl']}

        **Aufgabe:**
        - Vergleiche jede Nutzerantwort mit der Musterlösung.
        - Gib für jeden Teil (a₀/2, aₖ, bₖ) eine Bewertung von 0–5 Punkten **je Antwort + je Begründung**.
        - Gib zu jeder Bewertung eine kurze Begründung an.

        **Format:**
        Antwort a₀/2: <Punkte> – <Kommentar>  
        Begründung a₀/2: <Punkte> – <Kommentar>  
        Antwort aₖ: <Punkte> – <Kommentar>  
        Begründung aₖ: <Punkte> – <Kommentar>  
        Antwort bₖ: <Punkte> – <Kommentar>  
        Begründung bₖ: <Punkte> – <Kommentar>
        """



    elif question_type == "abtastung":
        message_content = f"""
        Die folgende Aufgabe betrifft das Abtasten einer periodischen Schwingung.

        Aufgabenteil 1:
        Antwort des Nutzers:
        fₐ: {user_inputs.get("fa_value")} {user_inputs.get("fa_unit")}
        Begründung: {user_inputs.get("expl1")}

        Musterlösung:
        fₐ: {solution_data['ideal_answers']['teil1_answer']} {solution_data['ideal_answers']['teil1_unit']}
        Begründung: {solution_data['ideal_answers']['teil1_expl']}

        Aufgabenteil 2:
        Antwort des Nutzers:
        fᵣ: {user_inputs.get("fr_value")} {user_inputs.get("fr_unit")}
        Begründung: {user_inputs.get("expl2")}

        Musterlösung:
        fᵣ: {solution_data['ideal_answers']['teil2_answer']} {solution_data['ideal_answers']['teil2_unit']}
        Begründung: {solution_data['ideal_answers']['teil2_expl']}

        **Aufgabe:**
        - Vergleiche jede der beiden Antworten mit der Musterlösung.
        - Bewerte pro Teilaufgabe:
            - die numerische Antwort (0–5 Punkte)
            - die Begründung (0–5 Punkte)
        - Gib bitte folgendes Format zurück:

        Teil 1 – Antwort: <Punkte> – <Kommentar>  
        Teil 1 – Begründung: <Punkte> – <Kommentar>  
        Teil 2 – Antwort: <Punkte> – <Kommentar>  
        Teil 2 – Begründung: <Punkte> – <Kommentar>
        """


    else:
        evaluation_instructions = """
               **Bewerte die Benutzerantwort auf einer Skala von 0-5**, basierend auf diesen Kriterien:
               - **Relevanz:** Trifft die Antwort genau auf die Frage zu?
               - **Korrektheit:** Enthält die Antwort inhaltlich korrekte Informationen?
               - **Detailtiefe:** Enthält die Antwort genug relevante Details?
               - **Vergleich mit der Musterlösung:** Ist sie ähnlich ausführlich?

               **Gib die Bewertung als eine Zahl (0-5) am Anfang der Antwort aus. Beispiel:**
               4. Die Antwort ist korrekt, aber nicht detailliert genug.
               """


        message_content = f"""
        Frage: {question}
        Musterlösung: {solution_data.get('ideal_answer', 'Nicht verfügbar')}
        Nutzerantwort: {user_inputs[0]}

        {evaluation_instructions}
        """

    print("📤 GPT-Thread wird gestartet...")
    thread = openai_client.beta.threads.create()
    openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
        instructions="Gib eine klare Bewertung (0-5) direkt am Anfang und begründe sie anschließend.",
        temperature=0.5
    )

    max_wait_time = 60
    start_time = time.time()
    while True:
        status = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if status.status == "completed":
            break
        elif status.status in ["failed", "cancelled"]:
            return None, "Fehler bei GPT-Auswertung."
        if time.time() - start_time > max_wait_time:
            return None, "Zeitüberschreitung bei GPT-Auswertung."
        time.sleep(2)

    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
    gpt_answer = messages.data[0].content[0].text.value
    score = extract_score_from_text(gpt_answer)

    return score, gpt_answer
