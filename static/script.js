document.addEventListener("DOMContentLoaded", async function () {
    console.log("📢 DOM geladen!");

    // Send-Button prüfen und Event-Listener hinzufügen
    const sendButton = document.getElementById("send-btn");
    if (!sendButton) {
        console.error("❌ FEHLER: Der Button mit ID 'send-btn' wurde nicht gefunden!");
    } else {
        if (!sendButton.dataset.listener) {
            console.log("✅ Button gefunden! Event wird hinzugefügt...");
            sendButton.addEventListener("click", function(event) {
                event.preventDefault(); // Doppelklick verhindern
                sendMessage();
            });
            sendButton.dataset.listener = "true";  // Verhindert mehrfaches Registrieren
        } else {
            console.warn("⚠️ sendMessage() wurde bereits registriert!");
        }
    }

    // "Nächste Frage"-Button prüfen und Event-Listener hinzufügen
    const nextQuestionButton = document.getElementById("next-question-btn");
    if (!nextQuestionButton) {
        console.error("❌ FEHLER: Der Button mit ID 'next-question-btn' wurde nicht gefunden!");
    } else {
        if (!nextQuestionButton.dataset.listener) {
            console.log("✅ 'Nächste Frage'-Button gefunden! Event wird hinzugefügt...");
            nextQuestionButton.addEventListener("click", loadNextQuestion);
            nextQuestionButton.dataset.listener = "true";
        } else {
            console.warn("⚠️ loadNextQuestion() wurde bereits registriert!");
        }
    }

    // Debug: Zeige alle IDs auf der Seite
    console.log("📌 Alle IDs auf der Seite:");
    document.querySelectorAll("[id]").forEach(el => console.log(el.id));

    // ✅ Erste Frage laden (await ist hier erlaubt)
    await loadNextQuestion();
});

////////////////////////////////////////////////////////////////////////////////////////

function getRatingColor(pct) {
    if (pct < 20) return "#e53935";  // rot
    if (pct < 40) return "#fb8c00";  // orange-rot
    if (pct < 60) return "#fdd835";  // gelb
    if (pct < 80) return "#9ccc65";  // hellgrün
    return "#43a047";                // grün
}

//////////////////////////////////////////////////////////////////////////////////////////

//Bezogen auf die Anzeige Button links
function resetFrageAnzeige() {
    const responseDiv = document.getElementById("response");
    const ratingDiv = document.getElementById("rating");
    const chatHistoryDiv = document.getElementById("chat-history");
    const idealAnswerDiv = document.getElementById("ideal-answer");
    const textInput = document.getElementById("text-answer");

    if (responseDiv) responseDiv.innerHTML = "<em>Warte auf Antwort...</em>";
    if (ratingDiv) ratingDiv.innerHTML = "Noch keine Bewertung...";
    if (chatHistoryDiv) chatHistoryDiv.innerHTML = "";
    if (idealAnswerDiv) idealAnswerDiv.innerHTML = "";
    if (textInput) textInput.value = "";

    // Zusätzliche Container ausblenden
    const tableContainer = document.getElementById("user-table-container");
    const textContainer = document.getElementById("open-text-answer");
    const imageContainer = document.getElementById("image-question-container");
    const dilemmaBContainer = document.getElementById("dilemma-b-container");
    const edgesmallContainer = document.getElementById("edgesmall-container");
    const edgesmall2Container = document.getElementById("edgesmall2-container");
    const hubauths1Container = document.getElementById("hubauths1-container");
    const signalklassiContainer = document.getElementById("signalklassi-container");
    const fourierContainer = document.getElementById("fourierreihe-container");
    const abtastungContainer = document.getElementById("abtastung-container");

    if (tableContainer) tableContainer.innerHTML = "";
    if (textContainer) textContainer.style.display = "none";
    if (imageContainer) imageContainer.style.display = "none";
    if (dilemmaBContainer) dilemmaBContainer.style.display = "none";
    if (edgesmallContainer) edgesmallContainer.style.display = "none";
    if (edgesmall2Container) edgesmall2Container.style.display = "none";
    if (hubauths1Container) hubauths1Container.style.display = "none";
    if (signalklassiContainer) signalklassiContainer.style.display = "none";
    if (fourierContainer) fourierContainer.style.display = "none";
    if (abtastungContainer) abtastungContainer.style.display = "none";
}

// Funktion zum Laden der nächsten Frage von der API
async function loadNextQuestion() {
    try {
        console.log("📌 loadNextQuestion() wurde aufgerufen!");

        const responseDiv = document.getElementById("response");
        const ratingDiv = document.getElementById("rating");
        const chatHistoryDiv = document.getElementById("chat-history");
        const idealAnswerDiv = document.getElementById("ideal-answer");
        const textInput = document.getElementById("text-answer");

        if (responseDiv) responseDiv.innerHTML = "<em>Warte auf Antwort...</em>";
        if (ratingDiv) ratingDiv.innerHTML = "Noch keine Bewertung...";
        if (chatHistoryDiv) chatHistoryDiv.innerHTML = "";
        if (idealAnswerDiv) idealAnswerDiv.innerHTML = "";
        if (textInput) textInput.value = "";

        const res = await fetch("/next-question");

        if (!res.ok) {
        throw new Error(`❌ API-Fehler! Status: ${res.status}`);
        }

        const data = await res.json();
        console.log("✅ API-Daten empfangen:", data);



        if (!data || (!data.question && data.question_type !== "HubAuths1" && data.question_type !== "abtastung")) {
        console.error("❌ Fehler: Keine gültige Frage empfangen!");
        document.getElementById("question").textContent = "⚠️ Fehler: Keine Frage gefunden!";
        return null;
        }


        // Fragetext oben setzen – je nach Typ
        if (data.question_type === "hubauths1") {
        document.getElementById("question").textContent = "Hubs and Authorities";
        } else if (data.question_type === "abtastung") {
        document.getElementById("question").textContent = data.intro;
        } else if (data.question_type !== "EA2_EdgeSmall_A1A2" && data.question_type !== "EA2_EdgeSmall_A3") {
        document.getElementById("question").textContent = data.question;
        } else {
        document.getElementById("question").textContent = "";
        }



        // Alle Container holen
        const tableContainer = document.getElementById("user-table-container");
        const textContainer = document.getElementById("open-text-answer");
        const imageContainer = document.getElementById("image-question-container");
        const dilemmaBContainer = document.getElementById("dilemma-b-container");
        const edgesmallContainer = document.getElementById("edgesmall-container");
        const edgesmall2Container = document.getElementById("edgesmall2-container");
        const hubauths1Container = document.getElementById("hubauths1-container");
        const signalklassiContainer = document.getElementById("signalklassi-container");
        const fourierContainer = document.getElementById("fourierreihe-container");
        const abtastungContainer = document.getElementById("abtastung-container");




        // Zurücksetzen / Verstecken
        tableContainer.innerHTML = "";
        textContainer.style.display = "none";
        imageContainer.style.display = "none";
        if (dilemmaBContainer) dilemmaBContainer.style.display = "none";
        if (edgesmallContainer) edgesmallContainer.style.display = "none";
        if (edgesmall2Container) edgesmall2Container.style.display = "none";
        if (hubauths1Container) hubauths1Container.style.display = "none";
        if (signalklassiContainer) signalklassiContainer.style.display = "none";
        if (fourierContainer) fourierContainer.style.display = "none";
        if (abtastungContainer) abtastungContainer.style.display = "none";



        if (data.question_type === "table" && data.table_data?.length > 0) {
            console.log("📊 Tabellenfrage erkannt.");
            renderTableQuestion(data.table_data);
        } else if (data.question_type === "single_questions") {
            console.log("🖼️ SingleFrage erkannt.");
            renderSingleQuestion(data);
        } else if (data.question_type === "image") {
            console.log("🖼️ Bildfrage erkannt.");
            imageContainer.style.display = "block";
            document.getElementById("image-question").src = data.image_path;
        } else if (data.question_type === "gefangenendilemma_a") {
            console.log("🎯 Gefangenendilemma A erkannt.");
            renderDilemmaMatrix(data.table_data);
        } else if (data.question_type === "gefangenendilemma_b") {
            console.log("🎯 Gefangenendilemma B erkannt.");
            if (dilemmaBContainer) dilemmaBContainer.style.display = "block";
        } else if (data.question_type === "parallelitaetabc") {
            console.log("📚 Parallelitätabc erkannt.");
            renderParallelitaetABC(data);
        } else if (data.question_type === "EA2_EdgeSmall_A1A2") {
            console.log("🧩 EdgeSmall-Aufgabe erkannt.");
            renderEdgeSmall(data);
        } else if (data.question_type === "EA2_EdgeSmall_A3") {
            console.log("🧠 EdgeSmall-Aufgabe Teil 3 erkannt.");
            renderEdgeSmall2(data);
        } else if (data.question_type === "hubauths1") {
            console.log("🔗 HubAuths1-Aufgabe erkannt.");
            renderHubAuths1(data);
        } else if (data.question_type === "signalklassi") {
            console.log("🔗 Signalklassi-Aufgabe erkannt.");
            renderSignalklassi(data);

        } else if (data.question_type === "fourier") {
            console.log("📈 Fourier-Aufgabe erkannt.");
            renderFourier(data);
        } else if (data.question_type === "abtastung") {
            console.log("🎯 Abtastung-Aufgabe erkannt.");
            renderAbtastung(data);


}

        return data;
    } catch (err) {
        console.error("❌ Fehler beim Laden der neuen Frage:", err);
        return null;
    }
}

function renderTableQuestion(tableData) {
    const container = document.getElementById("user-table-container");
    container.style.display = "block"; // Container sichtbar machen

    // Optional: Frage anzeigen, wenn Feld leer
    const q = document.getElementById("question");
    if (!q.textContent || q.textContent.trim() === "" || q.textContent === "Lade Frage...") {
        q.textContent = "Bestimmen Sie die Kennzahlen für folgende Topologien:";
    }

    let tableHTML = `
        <table border="1" style="margin-top: 15px; width: 100%; table-layout: fixed;">
            <tr>
                <th style="padding: 8px; vertical-align: middle;">Topologie</th>
                <th style="padding: 8px; vertical-align: middle;">Clusterkoeffizient</th>
                <th style="padding: 8px; vertical-align: middle;">Durchmesser</th>
            </tr>
    `;

    tableData.forEach(row => {
        tableHTML += `
            <tr>
                <td style="padding: 8px; vertical-align: middle; word-wrap: break-word; white-space: normal;">
                    ${row.topology}
                </td>
                <td style="padding: 8px; vertical-align: middle;">
                    <input type="text" class="cluster-input" data-topology="${row.topology}" style="width: 100%;">
                </td>
                <td style="padding: 8px; vertical-align: middle;">
                    <input type="text" class="diameter-input" data-topology="${row.topology}" style="width: 100%;">
                </td>
            </tr>`;
    });

    tableHTML += `</table>`;
    container.innerHTML = tableHTML;
}

function renderDilemmaMatrix(data) {
    const container = document.getElementById("user-table-container");
    container.style.display = "block";

    container.innerHTML = `
        <div style="margin-bottom: 20px;">
            <h3 style="color: #003366;">Gefangenendilemma</h3>
            <p>Ein dem Gefangenendilemma ähnliches Problem ist das sogenannte <em>Lift-Dilemma</em>, das sich wie folgt beschreiben lässt:</p>
            <p>Zwei Nachbarn (A und B) hören gerne laut bei offenem Fenster Heavy Metal und können sich in ihrem Genuss gegenseitig stören.</p>
            <p>Folgende Kombinationen sind dabei denkbar:</p>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
                <tr><td><strong>Kombination R</strong></td><td>Keiner hört Musik</td><td>beide erhalten 3 Genuss­punkte</td></tr>
                <tr><td><strong>Kombination S</strong></td><td><em>B</em> hört Musik, <em>A</em> nicht</td><td><em>B</em> erhält 8 Genuss­punkte, <em>A</em> keinen</td></tr>
                <tr><td><strong>Kombination T</strong></td><td><em>A</em> hört Musik, <em>B</em> nicht</td><td><em>A</em> erhält 8 Genuss­punkte, <em>B</em> keinen</td></tr>
                <tr><td><strong>Kombination P</strong></td><td>Beide hören Musik</td><td>beide erhalten 1 Genuss­punkt</td></tr>
            </table>
        </div>

        <h4>a) Füllen Sie nachfolgende Entscheidungstabelle aus!</h4>

        <table style="border-collapse: collapse; width: 100%; text-align: center; font-family: sans-serif;">
            <thead>
                <tr style="background-color: #375e72; color: white;">
                    <th style="padding: 6px; background-color: #0099cc; color: white;">A</th>
                    <th style="padding: 6px;">B</th>
                    <th colspan="2" style="padding: 6px;">ist still</th>
                    <th colspan="2" style="padding: 6px;">hört Musik</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: #0099cc; color: white;">
                    <th rowspan="2" style="padding: 6px;">ist still</th>
                    <td style="background-color: #375e72;"></td>
                    <td colspan="2" style="color: black; background-color: white;">
                        R = (
                        <input type="number" name="R_A" style="width: 40px; margin: 0 2px;">,
                        <input type="number" name="R_B" style="width: 40px; margin: 0 2px;"> )
                        <br>Gesamt:
                        <input type="number" name="R_G" style="width: 60px; margin-left: 4px;">
                    </td>
                    <td colspan="2" style="color: black; background-color: white;">
                        S = (
                        <input type="number" name="S_A" style="width: 40px; margin: 0 2px;">,
                        <input type="number" name="S_B" style="width: 40px; margin: 0 2px;"> )
                        <br>Gesamt:
                        <input type="number" name="S_G" style="width: 60px; margin-left: 4px;">
                    </td>
                </tr>
                <tr style="background-color: #0099cc; color: white;">
                    <th style="padding: 6px;">hört Musik</th>
                    <td colspan="2" style="color: black; background-color: white;">
                        T = (
                        <input type="number" name="T_A" style="width: 40px; margin: 0 2px;">,
                        <input type="number" name="T_B" style="width: 40px; margin: 0 2px;"> )
                        <br>Gesamt:
                        <input type="number" name="T_G" style="width: 60px; margin-left: 4px;">
                    </td>
                    <td colspan="2" style="color: black; background-color: white;">
                        P = (
                        <input type="number" name="P_A" style="width: 40px; margin: 0 2px;">,
                        <input type="number" name="P_B" style="width: 40px; margin: 0 2px;"> )
                        <br>Gesamt:
                        <input type="number" name="P_G" style="width: 60px; margin-left: 4px;">
                    </td>
                </tr>
            </tbody>
        </table>

        <p style="margin-top: 10px; font-style: italic;">Bitte tragen Sie die Werte für A, B und Gesamt manuell ein (insgesamt 12 Felder).</p>
    `;
}

function renderParallelitaetABC(data) {
    const container = document.getElementById("parallelitaet-container");
    container.style.display = "block"; // sichtbar machen
    container.innerHTML = `
        <p><strong>${data.step1_prompt}</strong></p>
        <textarea id="input-step1" rows="3" placeholder="Formel eingeben..."></textarea>

        <p><strong>${data.step2_prompt}</strong></p>
        <textarea id="input-step2" rows="3" placeholder="Variablen und Bedeutung..."></textarea>

        <p><strong>${data.step3_prompt}</strong></p>
        <textarea id="input-step3" rows="3" placeholder="Antwort zu Amdahls Gesetz..."></textarea>

        <p><strong>${data.step4_prompt}</strong></p>
        <textarea id="input-step4" rows="3" placeholder="Antwort zu Schwächen..."></textarea>
    `;
}

function renderHubAuths1(data) {
console.log("📄 Debug Frage:", data.question);

    currentQuestionType = "hubauths1";
    currentQuestion = data.question || "";

    const container = document.getElementById("hubauths1-container");
    container.style.display = "block";

    // Setze nur die statischen Texte/Bilder
    document.getElementById("hubauths1-image").src = "static/" + data.image_path;
    document.getElementById("hubauths1-sub1").textContent = data.subquestion1;
    document.getElementById("hubauths1-sub2").textContent = data.subquestion2;

    // Leere alle Eingabefelder vollständig
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            document.getElementById(`adj-${i}${j}`).value = "";
        }
    }

    document.getElementById("input-eigenvalue").value = "";
    document.getElementById("input-eigenvalue-expl").value = "";

    document.getElementById("input-hub1").value = "";
    document.getElementById("input-hub2").value = "";
    document.getElementById("input-hub3").value = "";
    document.getElementById("input-hub-expl").value = "";

    document.getElementById("input-auth1").value = "";
    document.getElementById("input-auth2").value = "";
    document.getElementById("input-auth3").value = "";
    document.getElementById("input-auth-expl").value = "";
}


function renderEdgeSmall(data) {
    const container = document.getElementById("edgesmall-container");
    if (!container) {
        console.error("❌ Container für EdgeSmall wurde nicht gefunden!");
        return;
    }

    container.style.display = "block";

    // Hauptfrage
    const questionEl = document.getElementById("edgesmall-question");
    if (questionEl) questionEl.textContent = data.question || "";

    // Teilfragen anzeigen
    const labelA = document.getElementById("edgesmall-sub-a-label");
    const labelB = document.getElementById("edgesmall-sub-b-label");

    if (labelA) labelA.textContent = data.subquestion_a || "Teilaufgabe a)";
    if (labelB) labelB.textContent = data.subquestion_b || "Teilaufgabe b)";

    // Eingabefelder zurücksetzen
    const inputA = document.getElementById("edge-a-answer");
    const explA = document.getElementById("edge-a-explanation");
    const inputB = document.getElementById("edge-b-answer");
    const explB = document.getElementById("edge-b-explanation");

    if (inputA) inputA.value = "";
    if (explA) explA.value = "";
    if (inputB) inputB.value = "";
    if (explB) explB.value = "";

    // Musterlösung anzeigen
    const idealA = document.getElementById("ideal-a");
    const idealAExpl = document.getElementById("ideal-a-expl");
    const idealB = document.getElementById("ideal-b");
    const idealBExpl = document.getElementById("ideal-b-expl");

    if (idealA) idealA.textContent = `a) Lösung: ${data.solution_a || "–"}`;
    if (idealAExpl) idealAExpl.textContent = `a) Erklärung: ${data.explanation_a || "–"}`;
    if (idealB) idealB.textContent = `b) Lösung: ${data.solution_b || "–"}`;
    if (idealBExpl) idealBExpl.textContent = `b) Erklärung: ${data.explanation_b || "–"}`;
}




function renderEdgeSmall2(data) {
    const container = document.getElementById("edgesmall2-container");
    if (!container) {
        console.error("❌ Container für EdgeSmall2 wurde nicht gefunden!");
        return;
    }

    container.style.display = "block";

    // Hauptfrage anzeigen
    const questionEl = document.getElementById("edgesmall2-question");
    if (questionEl) questionEl.textContent = data.question || "";

    // Labels für Teilaufgaben
    const labelA = document.getElementById("edgesmall2-sub-a-label");
    const labelB = document.getElementById("edgesmall2-sub-b-label");
    const labelC = document.getElementById("edgesmall2-sub-c-label");

    if (labelA) labelA.textContent = data.sub_a_label || "Neue mittlere Pfadlänge:";
    if (labelB) labelB.textContent = data.sub_b_label || "Rechenweg:";
    if (labelC) labelC.textContent = data.sub_c_label || "Vergleich zu Teil 2:";

    // Eingabefelder zurücksetzen
    const inputA = document.getElementById("edge2-a-answer");
    const inputB = document.getElementById("edge2-b-answer");
    const inputC = document.getElementById("edge2-c-answer");

    if (inputA) inputA.value = "";
    if (inputB) inputB.value = "";
    if (inputC) inputC.value = "";

    // Musterlösungen anzeigen
    const idealA = document.getElementById("ideal-a");
    const idealB = document.getElementById("ideal-b");
    const idealC = document.getElementById("ideal-c");

    if (idealA) idealA.textContent = `a): ${data.ideal_a || "–"}`;
    if (idealB) idealB.textContent = `b): ${data.ideal_b || "–"}`;
    if (idealC) idealC.textContent = `c): ${data.ideal_c || "–"}`;
}


function renderSingleQuestion(data) {
    console.log("📥 Single-Frage empfangen:", data.question); // Debug-Ausgabe

    document.getElementById("question").textContent = data.question;

    const openTextDiv = document.getElementById("open-text-answer");
    const textArea = document.getElementById("text-answer");

    if (openTextDiv && textArea) {
        openTextDiv.style.display = "block";
        textArea.value = "";  // Eingabefeld leeren
    } else {
        console.error("❌ Eingabefeld für offene Textfrage nicht gefunden!");
    }

    currentQuestionType = "single_questions";
    currentQuestion = data.question;
}

function renderSignalklassi(data) {
    console.log("📷 Bildpfade empfangen:", data.image_paths);

    const container = document.getElementById("signalklassi-container");
    if (!container) {
        console.error("❌ signalklassi-container nicht gefunden!");
        return;
    }

    container.style.display = "block";

    // Eingabefelder zurücksetzen
    for (let i = 1; i <= 7; i++) {
        const input = document.getElementById(`signal-input-${i}`);
        if (input) input.value = "";
    }

    // Bilder setzen
    const imageElements = [
        "signalklassi-img-1",
        "signalklassi-img-2",
        "signalklassi-img-3",
        "signalklassi-img-4",
        "signalklassi-img-5"
    ];

    imageElements.forEach((id, index) => {
        const img = document.getElementById(id);
        if (img && data.image_paths[index]) {
            img.src = "static/" + data.image_paths[index];
        } else if (img) {
            img.src = ""; // leeren, wenn kein Pfad vorhanden
        }
    });

    // Frage anzeigen
    document.getElementById("question").textContent = data.question;
    currentQuestionType = "signalklassi";
    currentQuestion = data.question;
}

function renderAbtastung(data) {
    const container = document.getElementById("abtastung-container");
    if (!container) {
        console.error("❌ abtastung-container nicht gefunden!");
        return;
    }

    container.style.display = "block";
    currentQuestionType = "abtastung";
    currentQuestion = data.intro;

    // Verwende die Felder wie aus der Datenbank
    document.getElementById("abtastung-intro").textContent = data.intro;
    document.getElementById("abtastung-sub1").innerHTML = "<strong>Aufgabenteil 1:</strong><br>" + data.teil1_prompt;
    document.getElementById("abtastung-sub2").innerHTML = "<strong>Aufgabenteil 2:</strong><br>" + data.teil2_prompt;

    ["fa-wert", "fa-einheit", "fr-wert", "fr-einheit", "expl1", "expl2"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
}

// ✅ Separat und korrekt: renderFourier()
function renderFourier(data) {
    const container = document.getElementById("fourierreihe-container");
    if (!container) {
        console.error("❌ fourierreihe-container nicht gefunden!");
        return;
    }

    container.style.display = "block";
    currentQuestionType = "fourier";
    currentQuestion = data.question;

    document.getElementById("question").textContent = data.question;
    document.getElementById("fourier-image").src = "static/pictures_for_questions/fourier.png";
    document.getElementById("fourier-hint").textContent = data.hint;
    document.getElementById("fourier-tip").textContent = data.tip;

    for (let i = 1; i <= 6; i++) {
        const input = document.getElementById(`fourier-input-${i}`);
        if (input) input.value = "";
    }
}

// Automatische Berechnung deaktiviert – Funktion bleibt leer
function updateCellSum(kombi) {
    // keine automatische Berechnung mehr
}

// Funktion für Bildfragen
function renderImageQuestion(question, imagePath) {
    let container = document.getElementById("user-table-container");
    container.innerHTML = `<img src="${imagePath}" alt="Fragebild" style="max-width: 100%;"><br>
                           <textarea id="image-answer" rows="4" cols="50" placeholder="Antwort hier eingeben..."></textarea>`;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Funktion zum Senden der Benutzerantwort an den Server
  async function sendMessage() {
    console.log("📤 sendMessage() wurde aufgerufen!");

    const responseDiv = document.getElementById("response");
    const ratingDiv = document.getElementById("rating");
    responseDiv.innerHTML = "<em>Antwort wird geladen...</em>";
    ratingDiv.innerHTML = "<em>Bewertung wird geladen...</em>";

    let question = "";


    if (currentQuestionType === "EA2_EdgeSmall_A1A2") {
        question = document.getElementById("edgesmall-question")?.textContent.trim();
    } else if (currentQuestionType === "EA2_EdgeSmall_A3") {
        question = document.getElementById("edgesmall2-question")?.textContent.trim();
    } else if (currentQuestionType === "abtastung") {
        question = document.getElementById("abtastung-intro")?.textContent.trim();
    } else {
        question = document.getElementById("question")?.textContent.trim();
    }

    console.log("📎 Frageinhalt (question):", question);



    const questionType = currentQuestionType;
    let userInputs;

    // 🔍 Eingaben sammeln je nach Fragetyp
    switch (questionType) {

        case "table":
            const rows = document.querySelectorAll("#user-table-container tr");
            userInputs = [];

            rows.forEach(row => {
                const topology = row.querySelector("td")?.textContent?.trim();
                if (!topology) return;

                const clusterInput = row.querySelector(".cluster-input");
                const diameterInput = row.querySelector(".diameter-input");

                if (clusterInput && diameterInput) {
                    userInputs.push({
                        topology: topology,
                        cluster: clusterInput.value.trim(),
                        diameter: diameterInput.value.trim()
                    });
                }
            });
            break;



        case "EA2_EdgeSmall_A1A2":
            userInputs = {
                a_answer: document.getElementById("edge-a-answer")?.value.trim(),
                a_explanation: document.getElementById("edge-a-explanation")?.value.trim(),
                b_answer: document.getElementById("edge-b-answer")?.value.trim(),
                b_explanation: document.getElementById("edge-b-explanation")?.value.trim()
            };
            break;

        case "EA2_EdgeSmall_A3":
            userInputs = {
                a_answer: document.getElementById("edge2-a-answer")?.value.trim(),
                b_answer: document.getElementById("edge2-b-answer")?.value.trim(),
                c_answer: document.getElementById("edge2-c-answer")?.value.trim()
            };
            break;


        case "parallelitaetabc":
            userInputs = [
                document.getElementById("input-step1")?.value.trim(),
                document.getElementById("input-step2")?.value.trim(),
                document.getElementById("input-step3")?.value.trim(),
                document.getElementById("input-step4")?.value.trim()
            ];
            break;

        case "hubauths1":
            const matrixRows = [];
            for (let i = 0; i < 3; i++) {
                const row = [];
                for (let j = 0; j < 3; j++) {
                    const input = document.getElementById(`adj-${i}${j}`);
                    row.push(input?.value.trim() || "");  // leeres Feld bleibt leer
                }
                matrixRows.push(row.join(","));  // z. B. "0,1,0"
            }

            userInputs = {
                adj_matrix: matrixRows.join(";"),
                eigenvalue: document.getElementById("input-eigenvalue")?.value.trim(),
                eigenvalue_explanation: document.getElementById("input-eigenvalue-expl")?.value.trim(),
                hub_vector: [
                    document.getElementById("input-hub1")?.value.trim(),
                    document.getElementById("input-hub2")?.value.trim(),
                    document.getElementById("input-hub3")?.value.trim()
                ],
                hub_explanation: document.getElementById("input-hub-expl")?.value.trim(),
                authority_vector: [
                    document.getElementById("input-auth1")?.value.trim(),
                    document.getElementById("input-auth2")?.value.trim(),
                    document.getElementById("input-auth3")?.value.trim()
                ],
                authority_explanation: document.getElementById("input-auth-expl")?.value.trim()
            };
            break;




        case "signalklassi":
        userInputs = [
            document.getElementById("signal-input-1")?.value.trim(),
            document.getElementById("signal-input-2")?.value.trim(),
            document.getElementById("signal-input-3")?.value.trim(),
            document.getElementById("signal-input-4")?.value.trim(),
            document.getElementById("signal-input-5")?.value.trim(),
            document.getElementById("signal-input-6")?.value.trim(),
            document.getElementById("signal-input-7")?.value.trim()
            ];
            break;


        case "gefangenendilemma_a":
            userInputs = {
                R: [
                    document.querySelector('input[name="R_A"]')?.value.trim(),
                    document.querySelector('input[name="R_B"]')?.value.trim(),
                    document.querySelector('input[name="R_G"]')?.value.trim()
                ],
                S: [
                    document.querySelector('input[name="S_A"]')?.value.trim(),
                    document.querySelector('input[name="S_B"]')?.value.trim(),
                    document.querySelector('input[name="S_G"]')?.value.trim()
                ],
                T: [
                    document.querySelector('input[name="T_A"]')?.value.trim(),
                    document.querySelector('input[name="T_B"]')?.value.trim(),
                    document.querySelector('input[name="T_G"]')?.value.trim()
                ],
                P: [
                    document.querySelector('input[name="P_A"]')?.value.trim(),
                    document.querySelector('input[name="P_B"]')?.value.trim(),
                    document.querySelector('input[name="P_G"]')?.value.trim()
                ]
            };
            break;



        case "gefangenendilemma_b":
            userInputs = {
                A: Array.from(document.querySelectorAll(".input-A")).map(input => input.value.trim()),
                B: Array.from(document.querySelectorAll(".input-B")).map(input => input.value.trim()),
                A_sum: document.getElementById("A_sum")?.value.trim(),
                B_sum: document.getElementById("B_sum")?.value.trim()
            };
            break;

        case "fourier":
            userInputs = [
                document.getElementById("fourier-input-1")?.value.trim(),
                document.getElementById("fourier-input-2")?.value.trim(),
                document.getElementById("fourier-input-3")?.value.trim(),
                document.getElementById("fourier-input-4")?.value.trim(),
                document.getElementById("fourier-input-5")?.value.trim(),
                document.getElementById("fourier-input-6")?.value.trim()
            ];
            break;

        case "abtastung":
            userInputs = {
                fa_value: document.getElementById("fa-wert")?.value.trim(),
                fa_unit: document.getElementById("fa-einheit")?.value.trim(),
                expl1: document.getElementById("expl1")?.value.trim(),
                fr_value: document.getElementById("fr-wert")?.value.trim(),
                fr_unit: document.getElementById("fr-einheit")?.value.trim(),
                expl2: document.getElementById("expl2")?.value.trim()
            };
            break;


        case "single_questions":
            userInputs = [document.getElementById("text-answer")?.value.trim()];
            console.log("📝 Nutzerantwort:", userInputs[0]);
            break;

        case "image":
            break;

        default:
            console.warn("⚠️ Unbekannter Fragetyp:", questionType);
            break;
    }

    console.log("📌 Frage:", question);
    console.log("📌 Fragetyp:", questionType);
    console.log("📌 Eingaben:", userInputs);




    console.log("🧪 Validierungstyp:", typeof userInputs, Array.isArray(userInputs) ? "Array" : "Objekt");
    console.log("🧪 userInputs-Werte:", Object.entries(userInputs));



if (
    !question ||
    !questionType ||
    (
        typeof userInputs === "object" &&
        !Array.isArray(userInputs) &&
        Object.values(userInputs).every(val => {
            if (typeof val === "string") {
              return val.trim() === "";
            }
            if (Array.isArray(val)) {
            return val.every(entry => typeof entry === "string" && entry.trim() === "");
            }
            return false;
        }))


 ) {
    console.error("❌ Ungültige Eingaben:", userInputs);
    responseDiv.innerHTML = "<strong>FEHLER:</strong> Ungültige Eingaben!";
    return;
   }

console.log("📤 Frage:", currentQuestion);
console.log("📤 Fragetyp:", currentQuestionType);
console.log("📤 Eingaben:", userInputs);


    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question,
                user_inputs: userInputs,
                question_type: questionType
            })
        });

        if (!res.ok) throw new Error(`❌ Serverfehler: ${res.status}`);

        const data = await res.json();
        console.log("✅ Serverantwort empfangen:", data);

        const idealAnswerDiv = document.getElementById("ideal-answer");
        if (idealAnswerDiv) {
            let solutionHTML = "";

        console.log("🧪 Daten zur Musterlösung:", data);

            switch (questionType) {
                case "single_questions":
                if (data.gpt_response?.score >= 4) {
                    solutionHTML = data.ideal_answer || "Keine Musterlösung verfügbar.";
                } else {
                   // solutionHTML = "<em>Die Musterlösung wird erst bei einer Bewertung von mindestens 4 Punkten angezeigt. </em>";

                    solutionHTML = `
                        <em>Die Musterlösung wird erst bei einer Bewertung von mindestens 4 Punkten angezeigt.</em><br>
                        <span style="font-size: 0.95em; color: #444;">
                        Zur weiteren Hilfestellung zu dieser Frage siehe auch Skript Kurseinheit X, Seite X.
                        </span>
                    `;
                }
                break;




                case "image":
                    solutionHTML = data.ideal_answer || "Keine Musterlösung verfügbar.";
                    break;

                case "parallelitaetabc":
                    solutionHTML = `
                        <strong>1. Formel:</strong> ${data.step1_ideal}<br>
                        <strong>2. Variablen:</strong> ${data.step2_ideal}<br>
                        <strong>3. Amdahl:</strong> ${data.step3_ideal}<br>
                        <strong>4. Schwächen:</strong> ${data.step4_ideal}<br>`;
                    break;


                case "EA2_EdgeSmall_A1A2":
                    solutionHTML = `
                        <strong>a) Antwort:</strong> ${data.solution_a}<br>
                        <strong>a) Rechenweg:</strong> ${data.explanation_a}<br><br>
                        <strong>b) Antwort:</strong> ${data.solution_b}<br>
                        <strong>b) Rechenweg:</strong> ${data.explanation_b}<br>`;
                    break;


                case "EA2_EdgeSmall_A3":
                    solutionHTML = `
                        <strong>a):</strong> ${data.ideal_a || "-"}<br>
                        <strong>b):</strong> ${data.ideal_b || "-"}<br>
                        <strong>c):</strong> ${data.ideal_c || "-"}<br>`;
                    break;

                case "hubauths1":
                    solutionHTML = `
                        <strong>Adjazenzmatrix:</strong><br>${data.adj_matrix}<br><br>
                        <strong>Eigenwert:</strong> ${data.eigenvalue}<br>
                        <strong>Erklärung m:</strong> ${data.eigenvalue_explanation}<br>
                        <strong>Hub-Vektor:</strong> ${data.hub_vector?.join(", ")}<br>
                        <strong>Erklärung h:</strong> ${data.hub_explanation}<br>
                        <strong>Authority-Vektor:</strong> ${data.authority_vector?.join(", ")}<br>
                        <strong>Erklärung a:</strong> ${data.authority_explanation}<br>`;
                    break;


                case "signalklassi":
                    solutionHTML = "<strong>Musterlösungen:</strong><br>";
                    if (Array.isArray(data.ideal_answers)) {
                        data.ideal_answers.forEach((answer, index) => {
                            solutionHTML += `Eingabe ${index + 1}: ${answer}<br>`;
                        });
                    } else {
                        solutionHTML += "Keine Musterlösungen vorhanden.";
                    }
                    break;


                case "fourier":
                    solutionHTML = `
                        <strong>a₀/2:</strong> ${data.ideal_answers.a0}<br>
                        <strong>Begründung a₀/2:</strong> ${data.ideal_answers.a0_expl}<br><br>

                        <strong>aₖ:</strong> ${data.ideal_answers.ak}<br>
                        <strong>Begründung aₖ:</strong> ${data.ideal_answers.ak_expl}<br><br>

                        <strong>bₖ:</strong> ${data.ideal_answers.bk}<br>
                        <strong>Begründung bₖ:</strong> ${data.ideal_answers.bk_expl}<br>
                        `;
                    break;

                case "abtastung":
                    solutionHTML = `
                        <strong>fₐ:</strong> ${data.solution_fa} ${data.solution_fa_unit}<br>
                        <strong>Begründung:</strong> ${data.solution_expl1}<br><br>
                        <strong>fᵣ:</strong> ${data.solution_fr} ${data.solution_fr_unit}<br>
                        <strong>Begründung:</strong> ${data.solution_expl2}<br>`;
                    break;

                case "table":
                    solutionHTML = "<strong>Idealwerte (Cluster/Durchmesser):</strong><br>";
                        if (Array.isArray(data.table_data)) {
                            data.table_data.forEach(row => {
                                solutionHTML += `${row.topology}: Cluster = ${row.cluster}, Durchmesser = ${row.diameter}<br>`;
                            });
                        } else {
                            solutionHTML += "Keine Musterlösung verfügbar.";
                        }
                    break;


                case "gefangenendilemma_b":
                solutionHTML = `
                    <strong>Ideale Strategie A:</strong><br>${(data.ideal_strategy_a || []).join(", ")}<br><br>
                    <strong>Ideale Strategie B:</strong><br>${(data.ideal_strategy_b || []).join(", ")}<br><br>
                    <strong>Genusspunkte A gesamt:</strong> ${data.total_score_a || "-"}<br>
                    <strong>Genusspunkte B gesamt:</strong> ${data.total_score_b || "-"}<br>`;
                break;


                case "gefangenendilemma_a":
                    solutionHTML = "Diese Aufgabe enthält keine klassische Musterlösung.";
                    break;

                default:
                    solutionHTML = "Keine Musterlösung gefunden.";
                    break;
            }

            idealAnswerDiv.innerHTML = solutionHTML;
        }

        // Bewertung & Feedback
        if (["gefangenendilemma_a", "gefangenendilemma_b"].includes(questionType)) {
            responseDiv.innerHTML = `<pre>${JSON.stringify(data.gpt_response, null, 2)}</pre>`;

            let ratingHTML = "";
            let totalPoints = 0;
            const maxPerPlayer = (questionType === "gefangenendilemma_b") ? 6 : 3;

            Object.entries(data.gpt_response).forEach(([key, val]) => {
                const score = val.score || 0;
                totalPoints += score;

                ratingHTML += `
                    <p><strong>${key}:</strong> ${score}/${maxPerPlayer}</p>
                    <div style="background-color: #ddd; width: 100%; height: 6px; border-radius: 3px;">
                        <div style="width: ${(score / maxPerPlayer) * 100}%; height: 100%; background-color: ${getRatingColor((score / maxPerPlayer) * 100)}; border-radius: 3px;"></div>
                    </div>`;
            });

            const maxPoints = 12;
            const pct = Math.round((totalPoints / maxPoints) * 100);


            ratingHTML += `
                <hr>
                <p><strong>Gesamtpunktzahl:</strong> ${totalPoints} / ${maxPoints} (${pct}%)</p>
                <div style="background-color: #ddd; width: 100%; height: 12px; border-radius: 6px; margin-top: 5px;">
                    <div style="width: ${pct}%; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 6px;"></div>
                </div>`;

            ratingDiv.innerHTML = ratingHTML;


        }
        else if (questionType === "single_questions") {
            if (data.gpt_response?.comment !== undefined) {
                responseDiv.innerHTML = `<strong>Kommentar:</strong> ${data.gpt_response.comment}`;
                ratingDiv.innerHTML = `
                    <p><strong>Bewertung:</strong> ${data.gpt_response.score || 0}/5</p>
                    <div style="background-color: #ddd; width: 100%; height: 6px; border-radius: 3px;">
                        <div style="width: ${(data.gpt_response.score || 0) * 20}%; height: 100%; background-color: ${getRatingColor((data.gpt_response.score || 0) * 20)}; border-radius: 3px;"></div>
                    </div>
                `;
            } else {
                responseDiv.innerHTML = "<strong>⚠️ Keine verwertbare GPT-Antwort erhalten.</strong>";
                ratingDiv.innerHTML = "<em>Keine Bewertung verfügbar.</em>";
            }
            return; // ⬅️ verhindert, dass der Rest für andere Fragetypen läuft

        } else {
            if (data.gpt_response) {
                // Rückmeldung anzeigen: erst feedback, dann summary, sonst fallback

                if (["EA2_EdgeSmall_A1A2", "EA2_EdgeSmall_A3"].includes(questionType)) {
                    responseDiv.innerHTML = "<em>Aufgabenbewertung siehe unten.</em>";
                } else {
                    responseDiv.innerHTML =
                        data.gpt_response.feedback ||
                        data.gpt_response.summary ||
                        "<em>Keine Rückmeldung erhalten.</em>";
                }



                if (questionType === "table" && Array.isArray(data.gpt_response.rating)) {
                    displayRating(data.gpt_response.rating, questionType);

                    const ratingDetails = document.getElementById("rating-details");
                    if (ratingDetails && data.gpt_response.summary) {
                        ratingDetails.innerHTML = `<em>${data.gpt_response.summary}</em>`;
                    }
                } else {
                        displayRating(data.gpt_response, questionType);
                }

            } else {
                responseDiv.innerHTML = "<strong>⚠️ Keine verwertbare Antwort erhalten.</strong>";
                ratingDiv.innerHTML = "<em>Keine Bewertung verfügbar.</em>";
            }
        }
    } catch (err) {
        console.error("❌ Fehler beim Senden der Nachricht:", err);
        responseDiv.innerHTML = `<strong>Fehler:</strong> Verbindung zum Server fehlgeschlagen.`;
        ratingDiv.innerHTML = "<em>Keine Bewertung verfügbar.</em>";
    } // <-- ❗ dieser schließt den `try/catch`-Block

  } // <-- ❗ dieser schließt die Funktion `sendMessage()`

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function displayRating(ratingData, questionType) {
    console.log("📢 displayRating() aufgerufen mit:", ratingData, questionType);

    const ratingDiv = document.getElementById("rating");
    if (!ratingDiv) {
        console.error("❌ FEHLER: ratingDiv wurde nicht gefunden!");
        return;
    }

    if (ratingData === undefined || ratingData === null) {
        console.warn("⚠️ Keine Bewertung zum Anzeigen!");
        ratingDiv.innerHTML = "<em>Keine Bewertung verfügbar.</em>";
        return;
    }

    let ratingHTML = "<h3>Bewertungen:</h3><ul>";
    let totalPoints = 0;
    let maxPoints = 10;


    if (questionType === "table" && Array.isArray(ratingData)) {
        ratingData.forEach(item => {
              const score = item.score || 0;
              const comment = item.comment || "";
              const pct = (score / 5) * 100;

              totalPoints += score;
              maxPoints += 5;

              ratingHTML += `
                  <li style="margin-bottom: 15px;">
                      <strong>${item.topology}:</strong><br>
                      <em>Bewertung:</em> ${score}/5
                      <div style="background-color: #ddd; width: 100%; height: 6px; margin-top: 3px; border-radius: 3px;">
                          <div style="width: ${pct}%; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 3px;"></div>
                     </div>
                      <p style="margin-top: 5px;"><em>Kommentar:</em> ${comment}</p>
                  </li>
              `;
        });



    } else if (questionType === "gefangenendilemma_a") {
        for (const key in ratingData) {
            const score = ratingData[key].score;
            const pct = (score / 3) * 100;
            totalPoints += score;
            ratingHTML += `
                <li style="margin-bottom: 10px;">
                    <strong>${key}:</strong> ${score}/3
                    <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                        <div style="width: ${pct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                    </div>
                </li>`;
        }
        maxPoints = 4 * 3;

    } else if (questionType === "gefangenendilemma_b") {
        const maxScorePerPlayer = { strategy: 4, points: 2 };
        let aScore = 0;
        let bScore = 0;

        ["A", "B"].forEach(player => {
            const score = ratingData[player]?.score || 0;
            const comment = ratingData[player]?.comment || "";
            const strategyMatch = parseInt((comment.match(/Strategie: (\d)/) || [])[1] || 0);
            const pointsMatch = parseInt((comment.match(/Genusspunkte: (\d)/) || [])[1] || 0);
            const strategyPct = (strategyMatch / maxScorePerPlayer.strategy) * 100;
            const pointsPct = (pointsMatch / maxScorePerPlayer.points) * 100;

            if (player === "A") aScore = score;
            else bScore = score;

            totalPoints += score;

            ratingHTML += `
                <li style="margin-bottom: 12px;">
                    <strong>${player}:</strong> Strategie: ${strategyMatch}/4
                    <div style="background-color: #ddd; width: 100%; height: 8px; margin: 5px 0; border-radius: 4px;">
                        <div style="width: ${strategyPct}%; height: 100%; background-color: ${getRatingColor(strategyPct)}; border-radius: 4px;"></div>
                    </div>
                    Genusspunkte: ${pointsMatch}/2
                    <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                        <div style="width: ${pointsPct}%; height: 100%; background-color: ${getRatingColor(pointsPct)}; border-radius: 4px;"></div>
                    </div>
                </li>`;
        });

        maxPoints = 12;
        const finalPct = (totalPoints / maxPoints) * 100;
        ratingHTML += `
            <hr>
            <p><strong>Gesamtpunktzahl:</strong> ${totalPoints} / ${maxPoints} (${Math.round(finalPct)}%)</p>
            <div style="background-color: #ddd; width: 100%; height: 10px; border-radius: 4px;">
                <div style="width: ${finalPct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(finalPct)}; border-radius: 4px;"></div>
            </div>`;



    } else if (questionType === "parallelitaetabc") {
    for (const key in ratingData) {
        const entry = ratingData[key];
        const score = entry.score || 0;
        const comment = entry.comment || "";
        const pct = (score / 2) * 100;
        totalPoints += score;

        ratingHTML += `
            <li style="margin-bottom: 10px;">
                <strong>${key}:</strong> ${score}/2 – ${comment}
                <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                    <div style="width: ${pct}%; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                </div>
            </li>`;
    }
    maxPoints = 4 * 2;


    } else if (questionType === "EA2_EdgeSmall_A1A2") {
    for (const teil in ratingData) {
        const entry = ratingData[teil];
        const score = entry.score || 0;
        const comment = entry.comment || "";
        const pct = (score / 5) * 100;
        totalPoints += score;

        ratingHTML += `
            <li style="margin-bottom: 10px;">
                <strong>Teil ${teil}:</strong> ${score}/5 – ${comment}
                <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                    <div style="width: ${pct}%; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                </div>
            </li>`;
    }
    maxPoints = 10;


    } else if (questionType === "EA2_EdgeSmall_A3") {
    for (const teil in ratingData) {
        const entry = ratingData[teil];
        const score = entry.score || 0;
        const comment = entry.comment || "";
        const pct = (score / 2) * 100;
        totalPoints += score;

        ratingHTML += `
            <li style="margin-bottom: 10px;">
                <strong>Teil ${teil}:</strong> ${score}/2 – ${comment}
                <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                    <div style="width: ${pct}%; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                </div>
            </li>`;
    }
    maxPoints = 6;

    } else if (questionType === "hubauths1") {
    for (const teil in ratingData) {
        if (teil === "total_score") continue; // ⛔ Gesamtpunktzahl nicht einzeln anzeigen

        const entry = ratingData[teil];
        const score = entry.score || 0;
        const comment = entry.comment || "";

        const max = teil === "Matrix" ? 4.5 : 5;
        const pct = (score / max) * 100;
        totalPoints += score;
        maxPoints += max;

        ratingHTML += `
            <li style="margin-bottom: 10px;">
                <strong>Teil ${teil}:</strong> ${score}/${max} – ${comment}
                <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                    <div style="width: ${pct}%; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                </div>
            </li>`;
    }

    // Stelle sicher, dass die Gesamtpunktzahl korrekt ist (explizit auf 19.5 setzen, falls nötig)
    maxPoints = 19.5;


    } else if ([
        "single_questions",
        "image",
    ].includes(questionType) && typeof ratingData === "object" && "score" in ratingData) {
        totalPoints = ratingData.score;
        maxPoints = questionType === "single_questions" ? 5 : 10;
        const pct = (ratingData.score / maxPoints) * 100;
        ratingHTML += `
            <li style="margin-bottom: 10px;">
                <strong>Bewertung:</strong> ${ratingData.score}/${maxPoints}
                <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                    <div style="width: ${pct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                </div>
            </li>`;

    } else if (typeof ratingData === "number") {
        totalPoints = ratingData;
        maxPoints = questionType === "single_questions" ? 5 : 10;
        const pct = (ratingData / maxPoints) * 100;
        ratingHTML += `
            <li style="margin-bottom: 10px;">
                <strong>Bewertung:</strong> ${ratingData}/${maxPoints}
                <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                    <div style="width: ${pct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                </div>
            </li>`;

    } else if (questionType === "signalklassi") {
        for (const key in ratingData) {
            const entry = ratingData[key];
            const score = entry.score || 0;
            const comment = entry.comment || "";
            const pct = (score / 0.5) * 100;
            totalPoints += score;

            ratingHTML += `
                <li style="margin-bottom: 10px;">
                    <strong>${key}:</strong> ${score}/5 – ${comment}
                    <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                        <div style="width: ${pct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                    </div>
                </li>`;
        }
        maxPoints = 7 * 0.5;  // 7 Felder à 5 Punkte

    } else if (questionType === "fourier") {
        for (const key in ratingData) {
            const entry = ratingData[key];
            const score = entry.score || 0;
            const comment = entry.comment || "";
            const pct = (score / 5) * 100;
            totalPoints += score;

            ratingHTML += `
                <li style="margin-bottom: 10px;">
                    <strong>${key}:</strong> ${score}/5 – ${comment}
                    <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                        <div style="width: ${pct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                    </div>
                </li>`;
        }
        maxPoints = 6 * 5;


    } else if (questionType === "abtastung") {
        for (const key in ratingData) {
            const entry = ratingData[key];
            const score = entry.score || 0;
            const comment = entry.comment || "";
            const pct = (score / 5) * 100;
            totalPoints += score;

            ratingHTML += `
                <li style="margin-bottom: 10px;">
                    <strong>${key}:</strong> ${score}/5 – ${comment}
                    <div style="background-color: #ddd; width: 100%; height: 8px; margin-top: 5px; border-radius: 4px;">
                        <div style="width: ${pct}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(pct)}; border-radius: 4px;"></div>
                    </div>
                </li>`;
        }
        maxPoints = 6 * 5;



    } else {
        ratingHTML += "<li>⚠️ Unbekanntes Bewertungsformat.</li>";
        console.warn("⚠️ Unbekanntes Bewertungsformat:", ratingData);
    }

    const percentage = Number(((totalPoints / maxPoints) * 100).toFixed(1));
    ratingHTML += `</ul><p><strong>Gesamtpunktzahl:</strong> ${totalPoints} / ${maxPoints} (${percentage}%)</p>
        <div style="background-color: #ddd; width: 100%; height: 10px; border-radius: 5px;">
            <div style="width: ${percentage}%; min-width: 2px; height: 100%; background-color: ${getRatingColor(percentage)}; border-radius: 5px;"></div>
        </div><br>`;

    ratingDiv.innerHTML = ratingHTML;
}

////////////////////////////////////////////////////////////////////////////////////////

// Versteckt alle Fragen-Container
function hideAllQuestionContainers() {
    const containers = [
        "open-text-answer",
        "image-question-container",
        "user-table-container",
        "dilemma-b-container",
        "parallelitaet-container",
        "edgesmall-container",
        "edgesmall2-container",
        "hubauths1-container",
        "signalklassi-container",
        "fourierreihe-container",
        "abtastung-container"
    ];
    containers.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    });

    // Bild ausblenden, wenn keins geladen wird
    const image = document.getElementById("question-image");
    if (image) image.style.display = "none";
}

async function loadSpecificQuestion(type) {
    console.log("🎯 Lade spezifischen Fragetyp:", type);

    resetFrageAnzeige();
    hideAllQuestionContainers();  // Wichtig, damit vorherige Frageansicht ausgeblendet wird

    // 🧹 Reset von Antwort, Bewertung und Chat-Verlauf
    const gptAnswer = document.getElementById("gpt-answer");
    if (gptAnswer) gptAnswer.innerHTML = "<em>Warte auf Antwort...</em><br>Noch keine Bewertung...";

    const ratingDetails = document.getElementById("rating-details");
    if (ratingDetails) ratingDetails.innerHTML = "";

    const chatHistory = document.getElementById("chat-history");
    if (chatHistory) chatHistory.innerHTML = "";

    const ratingBar = document.getElementById("rating-bar");
    if (ratingBar) ratingBar.style.width = "0%";

    const ratingScore = document.getElementById("rating-score");
    if (ratingScore) ratingScore.textContent = "Bewertung: 0/5";

    const totalScore = document.getElementById("total-score");
    if (totalScore) totalScore.textContent = "Gesamtpunktzahl: 0 / 5 (0%)";

    // Frage vom Server laden
    const res = await fetch(`/next-question?type=${type}`);
    if (!res.ok) {
        alert("❌ Fehler beim Laden der Frage.");
        return;
    }

    const data = await res.json();
    console.log("✅ Frage empfangen:", data);

    if (!data || !data.question_type) {
        alert("⚠️ Keine gültige Frage gefunden.");
        return;
    }

      // 🔧 Wichtig: globale Variable setzen, damit sendMessage() weiß, was zu tun ist
    currentQuestionType = data.question_type;
    currentQuestion = data.question || "";

    // Frage anzeigen (außer bei EdgeSmall)
    if (data.question_type !== "EA2_EdgeSmall_A1A2" && data.question_type !== "EA2_EdgeSmall_A3") {
        document.getElementById("question").textContent = data.question || "";
    } else {
        document.getElementById("question").textContent = "";
    }

    // Passende Renderfunktion aufrufen oder direkt anzeigen
    switch (data.question_type) {
        case "gefangenendilemma_a":
            renderDilemmaMatrix(data.table_data);
            break;
        case "gefangenendilemma_b":
            const dilemmaBContainer = document.getElementById("dilemma-b-container");
            if (dilemmaBContainer) dilemmaBContainer.style.display = "block";
            break;
        case "signalklassi":
            renderSignalklassi(data);
            break;
        case "fourier":
            renderFourier(data);
            break;
        case "abtastung":
            renderAbtastung(data);
            break;
        case "parallelitaetabc":
            renderParallelitaetABC(data);
            break;
        case "EA2_EdgeSmall_A1A2":
            renderEdgeSmall(data);
            break;
        case "EA2_EdgeSmall_A3":
            renderEdgeSmall2(data);
            break;
        case "hubauths1":
            renderHubAuths1(data);
            break;
        case "single_questions":
            renderSingleQuestion(data);
            break;
        case "image":
            renderImageQuestion(data);
            break;
        case "table":
            renderTableQuestion(data.table_data);
            break;
        default:
            alert("❌ Unbekannter Fragetyp");
    }
}









