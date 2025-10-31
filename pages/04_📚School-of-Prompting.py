import streamlit as st
import openai
from openai import OpenAI
import db
import pw_check as pw
import parameters as par
import llm_provider
import chat_ui

 #Passwort checken
if pw.check_password() == False:
    st.stop()

# Inject modern chat UI CSS
chat_ui.inject_chat_css()

client = OpenAI()
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialisiere session_state-variablen
if "sop_bot" not in st.session_state:
    st.session_state["sop_bot"] = db.get_bot("Assistent")
    st.session_state["sop_bot_name"] = st.session_state.sop_bot["bot_name"]
    st.session_state["sop_sys_prompt"] = st.session_state.sop_bot["sys_prompt"]
    st.session_state["sop_model"] = st.session_state.sop_bot["model"]
    st.session_state["sop_model_if_error"] = st.session_state.sop_bot["model_if_error"]
    st.session_state["sop_temp"] = st.session_state.sop_bot["temp"]

if "teacher_bot" not in st.session_state:
    st.session_state["teacher_bot"] = db.get_bot("Teacher")
    st.session_state["teacher_bot_name"] = st.session_state.teacher_bot["bot_name"]
    st.session_state["teacher_sys_prompt"] = st.session_state.teacher_bot["sys_prompt"]
    st.session_state["teacher_temp"] = st.session_state.teacher_bot["temp"]
    st.session_state["teacher_model"] = st.session_state.teacher_bot["model"]
    st.session_state["teacher_model_if_error"] = st.session_state.teacher_bot["model_if_error"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.sop_sys_prompt}]

if "displayed_messages" not in st.session_state:
    st.session_state.displayed_messages = []

if "teacher_messages" not in st.session_state:
    st.session_state.teacher_messages = []

if "completed_exercises" not in st.session_state:
    st.session_state.completed_exercises = set()

# Display modern chat header
chat_ui.display_chat_header(
    bot_name="School-of-Prompting",
    model=st.session_state.sop_model if "sop_model" in st.session_state else None,
    description="🎯 KI-gestützte Arbeit in der Ergotherapie - datenschutzkonform und praxistauglich"
)

# Kurze, klare Einführung (immer sichtbar, kein Expander)
st.markdown("""
### 💡 Was macht die School of Prompting besonders?

**Übe hier nur, was du später auch wirklich so nutzen darfst.**

Alle Übungen sind datenschutzkonform und arbeiten **ohne Klientendaten**. Du lernst KI für:
- 📋 Informationsmaterialien erstellen
- 🔍 Fachkonzepte erschließen und Literatur aufbereiten
- 🎯 Therapieplanung vorbereiten (generisch)
- 🤔 Reflexion und Perspektivwechsel
""")

# Optionaler Expander für mehr Details
with st.expander("ℹ️ Mehr über Prompting-Techniken", False):
    st.markdown("""
    ### Die Techniken im Überblick
    
    **Zero-Shot:** Direkte Anweisung ohne Beispiele - für klare, strukturierte Aufgaben
    
    **One-Shot:** Ein Beispiel als Vorlage - für einheitliche Formate
    
    **Few-Shot:** Mehrere Beispiele zeigen das Muster - für komplexere Transformationen
    
    **Chain-of-Thought:** Schrittweise Denkprozesse - für komplexe Aufgaben
    
    **Skala:** Anpassung entlang einer Skala - für verschiedene Zielgruppen
    
    **Role:** Perspektivwechsel durch Rollenzuweisung - für Reflexion
    
    **Constraint:** Klare Begrenzungen setzen - für fokussierte Ergebnisse
    """)

# Dictionary mit Aufgabenstellungen
task_messages = {
    "Zero-Shot Prompting": {
        "Informationsblatt Ergonomie": {
            "task": """🎯 Lernziel: Entwickle einen präzisen Zero-Shot Prompt für ein Informationsblatt

**Aufgabe:**
Erstelle ein Informationsblatt zum Thema "Ergonomie am Arbeitsplatz" für eine Praxis oder WfbM.

**Experimentiere mit verschiedenen Aspekten:**
- Wie beeinflusst die **Zielgruppe** das Ergebnis? (z.B. Büroarbeiter vs. WfbM-Mitarbeiter)
- Was bewirkt eine **Längenvorgabe**? (z.B. "Eine DIN A4 Seite", "5 Tipps")
- Wie wirkt sich der **Sprachstil** aus? (z.B. "Kurz und knapp", "Motivierend", "Mit Beispielen")
- Was passiert bei **Strukturvorgaben**? (z.B. "Mit Überschriften", "Als Checkliste")

**Beispiel-Prompt zum Start:**
"Erstelle ein Informationsblatt über ergonomisches Sitzen am Arbeitsplatz für eine Werkstatt für Menschen mit Behinderung. Das Blatt soll eine DIN A4 Seite lang sein, in einfacher Sprache geschrieben und 5 konkrete Tipps enthalten."

✅ **Praxistauglich:** Du kannst solche Informationsblätter jederzeit für deine Praxis erstellen!""",
            "hint": "💭 Vergleiche die Ergebnisse bei unterschiedlichen Zielgruppen und Stilangaben. Was macht den größten Unterschied?",
        },
        "Traumreise": {
            "task": """🎯 Lernziel: Entwickle einen strukturierten Zero-Shot Prompt für therapeutische Inhalte

**Aufgabe:**
Erstelle eine kurze Traumreise (3-5 Minuten) als Einstieg für eine Gruppentherapie.

**Entscheide dich für:**
- **Zielgruppe:** Kinder? Erwachsene? Senior:innen? Menschen mit kognitiven Einschränkungen?
- **Thema:** Wald? Strand? Garten? Berge? Abstrakt (Farben, Formen)?
- **Zielsetzung:** Entspannung? Aktivierung? Ankommen in der Gruppe?

**Experimentiere mit der Struktur:**
- Offene Anfrage: "Erstelle eine Traumreise zum Thema Wald"
- Strukturierte Anfrage: "Erstelle eine Traumreise mit Einleitung, 3 Stationen und Rückholung"
- Mit Sprachvorgaben: "In einfacher, ruhiger Sprache"
- Mit Zeitangabe: "Für genau 5 Minuten Vorlesezeit"

**Beispiel-Prompt:**
"Erstelle eine 3-minütige Traumreise zum Thema 'Frühlingsgarten' für eine Seniorengruppe. Die Sprache soll ruhig und bildreich sein. Gliedere sie in: Ankommen, 3 Sinneserlebnisse, sanfte Rückholung."

✅ **Praxistauglich:** Solche Traumreisen kannst du für deine Gruppen vorbereiten!""",
            "hint": "💭 Achte darauf, wie die Detailtiefe deiner Anweisung das Ergebnis beeinflusst.",
        },
        "Beratungskonzept strukturieren": {
            "task": """🎯 Lernziel: Entwickle einen Zero-Shot Prompt für die Vorbereitung von Beratungen

**Aufgabe:**
Entwickle ein strukturiertes Konzept für ein Beratungsgespräch zu einem therapeutischen Thema.

**Mögliche Themen:**
- Gelenkschutz im Alltag (für Menschen mit Arthrose)
- Umgang mit Energiehaushalt (für Menschen mit chronischer Erschöpfung)  
- Sturzprophylaxe im häuslichen Umfeld (für Senior:innen)
- Konzentration bei Hausaufgaben (für Eltern von Kindern mit ADHS)
- Selbstständigkeit fördern (für Angehörige von Menschen mit Demenz)

**Experimentiere mit verschiedenen Strukturen:**
- "Erstelle einen Gesprächsleitfaden für..."
- "Strukturiere eine 30-minütige Beratung zu..."
- "Entwickle ein Beratungskonzept mit Einstieg, Hauptteil, Abschluss für..."

**Was soll enthalten sein?**
- Gesprächseinstieg / Warm-Up
- Kernbotschaften / Wissensvermittlung
- Praktische Tipps / Alltagsbeispiele
- Materialien zum Mitnehmen
- Gesprächsabschluss

**Beispiel-Prompt:**
"Erstelle ein Konzept für eine 20-minütige Angehörigenberatung zum Thema 'Gelenkschutz im Alltag bei Arthrose'. Gliedere es in: Einstieg, 5 Kernprinzipien mit Alltagsbeispielen, häufige Fragen, Abschluss."

✅ **Praxistauglich:** Diese Konzepte helfen dir, Beratungen strukturiert vorzubereiten!""",
            "hint": "💭 Ein klares Konzept hilft dir, in der Beratung nichts zu vergessen und professionell aufzutreten.",
        }
    },
    "One-Shot Prompting": {
        "Übungsanleitung erstellen": {
            "task": """🎯 Lernziel: Nutze One-Shot Prompting für einheitliche Formate

**Aufgabe:**
Du möchtest für verschiedene Übungen einheitliche Anleitungen erstellen. Gib der KI ein Beispiel als Vorlage.

**Beispiel-Anleitung (als Vorlage):**

---
**Übung: Münzen sortieren**

*Ziel:* Verbesserung der Feinmotorik und taktilen Wahrnehmung

*Material:* 
- Verschiedene Münzen (1ct bis 2€)
- Kleine Schälchen

*Durchführung:*
1. Münzen mischen und in eine Schale geben
2. Klient:in sortiert Münzen nach Wert in verschiedene Schälchen
3. Variation: Mit geschlossenen Augen nach Gefühl sortieren

*Schwierigkeitsgrade:*
- Einfach: Große Wertunterschiede (1ct, 1€, 2€)
- Mittel: Alle Münzwerte
- Schwer: Mit geschlossenen Augen

*Therapeutische Schwerpunkte:*
- Feinmotorische Präzision
- Taktile Diskrimination
- Konzentration

---

**Deine Aufgabe:**
Erstelle nach diesem Muster Anleitungen für andere Übungen:
- Knöpfe sortieren nach Größe
- Wäscheklammern an Karton befestigen
- Schrauben und Muttern zusammenfügen
- Perlen auf Schnur auffädeln

**Experimentiere:**
- Wie explizit muss der Hinweis auf die Vorlage sein?
- Reicht: "Erstelle nach diesem Muster..."
- Oder brauchst du: "Übernimm die Struktur mit Ziel, Material, Durchführung..."

**Beispiel-Prompt:**
"Erstelle nach dem Muster der obigen Übungsanleitung eine Anleitung für die Übung 'Wäscheklammern an Karton befestigen'. Behalte die Struktur mit Ziel, Material, Durchführung, Schwierigkeitsgraden und therapeutischen Schwerpunkten bei."

✅ **Praxistauglich:** Erstelle dir einen Pool an einheitlich formatierten Übungsanleitungen!""",
            "hint": "💭 One-Shot Prompting ist perfekt, um konsistente Formate für mehrere ähnliche Aufgaben zu erstellen.",
        },
        "Infomaterial-Serie": {
            "task": """🎯 Lernziel: Erstelle eine Serie von Materialien nach einheitlichem Muster

**Aufgabe:**
Entwickle eine Serie von Infomaterialien zu einem Thema, die alle die gleiche Struktur haben.

**Beispiel-Thema: Gelenkschutz**

**Beispiel-Info #1 (als Vorlage):**

---
**GELENKSCHUTZ IN DER KÜCHE** 🍳

*Warum ist das wichtig?*
In der Küche arbeiten wir oft mit Kraft und in ungünstigen Positionen. Das belastet die Gelenke unnötig.

*Die 3 wichtigsten Prinzipien:*
1. **Große Griffe nutzen:** Töpfe und Pfannen mit dicken Griffen schonen die Fingergelenke
2. **Beide Hände einsetzen:** Schwere Töpfe mit beiden Händen tragen verteilt die Last
3. **Hilfsmittel verwenden:** Elektrische Dosenöffner, Einhandrührgerät, rutschfeste Unterlagen

*Konkrete Alltagstipps:*
- Gläser mit beiden Händen öffnen (eine Hand hält, eine dreht)
- Flaschen mit Flaschenöffner statt mit purer Handkraft öffnen
- Messer mit dickem Griff und guter Schärfe verwenden

---

**Deine Aufgabe:**
Erstelle nach diesem Muster weitere Info-Karten für:
- Gelenkschutz im Bad
- Gelenkschutz im Garten
- Gelenkschutz bei Haushaltsarbeiten
- Gelenkschutz beim Einkaufen

**Experimentiere:**
- Wie konkret muss die Vorlage sein?
- Was passiert, wenn du nur sagst: "Mache noch eine für das Bad"?
- Was, wenn du explizit die Struktur benennst?

**Beispiel-Prompt:**
"Erstelle nach dem Muster der Info-Karte 'Gelenkschutz in der Küche' eine weitere Karte zum Thema 'Gelenkschutz im Bad'. Behalte die Struktur bei: Warum wichtig?, 3 Prinzipien, Konkrete Alltagstipps."

✅ **Praxistauglich:** So erstellst du einheitliche Info-Serien für deine Praxis!""",
            "hint": "💭 Eine Serie von Materialien mit einheitlichem Format wirkt professionell und ist für Klient:innen leichter zu nutzen.",
        }
    },
    "Few-Shot Prompting": {
        "Betätigungsanalyse": {
            "task": """🎯 Lernziel: Entwickle Few-Shot Prompts für strukturierte Analysen

**Aufgabe:**
Analysiere Betätigungen systematisch nach einem etablierten Muster.

**Beispiel-Analysen (als Vorlage):**

**1. Kaffee kochen**
- *Komponenten:* Wasser einfüllen, Filter einsetzen, Pulver dosieren, Maschine starten, warten, eingießen
- *Umweltfaktoren:* Arbeitshöhe, Wasserzugang, Steckdose, Bewegungsraum
- *Personenfaktoren:* Kraft, Feinmotorik, Sequenzplanung, Zeitverständnis
- *Bedeutung:* Morgenritual, Autonomie, Gastfreundschaft, sozialer Anlass

**2. Einkaufen gehen**
- *Komponenten:* Liste erstellen, Weg bewältigen, orientieren, Produkte finden, bezahlen, transportieren
- *Umweltfaktoren:* Entfernung, Verkehrsmittel, Geschäftslayout, Menschenmenge
- *Personenfaktoren:* Mobilität, Orientierung, Entscheidungsfähigkeit, Ausdauer, Kraft
- *Bedeutung:* Selbstversorgung, Autonomie, Teilhabe, Kompetenz

**3. Sich anziehen**
- *Komponenten:* Kleidung wählen, Reihenfolge planen, Verschlüsse öffnen/schließen, koordinieren, Balance halten
- *Umweltfaktoren:* Sitzgelegenheit, Schrank zugänglich, Kleidung verfügbar, Zeit
- *Personenfaktoren:* Feinmotorik, Grobmotorik, Planung, Gleichgewicht
- *Bedeutung:* Selbstbestimmung, soziale Norm, Selbstausdruck, Würde

**Deine Aufgabe:**
Erstelle nach diesem Muster Analysen für:
- Zähne putzen
- Telefonieren
- Kochen (ein einfaches Gericht)
- Wäsche aufhängen
- Sich schminken / rasieren
- Bus/Bahn fahren

**Experimentiere:**
- Wie viele Beispiele brauchst du mindestens? (Teste mit 1, 2, 3 Beispielen)
- Musst du die Kategorien erklären oder erkennt die KI das Muster?
- Was passiert, wenn du sehr unterschiedliche Betätigungen wählst?

**Beispiel-Prompt:**
"Analysiere nach dem Muster der drei obigen Beispiele die Betätigung 'Telefonieren'. Nutze die gleichen Kategorien: Komponenten, Umweltfaktoren, Personenfaktoren, Bedeutung."

✅ **Praxistauglich:** Betätigungsanalysen helfen dir, therapeutische Ansatzpunkte zu identifizieren!""",
            "hint": "💭 Die KI erkennt das Muster aus den Beispielen. Je konsistenter deine Beispiele, desto besser das Ergebnis.",
        },
        "Aktivitätenpool erstellen": {
            "task": """🎯 Lernziel: Nutze Few-Shot für kreative Ideensammlungen

**Aufgabe:**
Erstelle einen Pool therapeutischer Aktivitäten für verschiedene Betätigungsziele - ohne konkrete Klient:innen!

**Beispiele für: Betätigung "Einkaufen"**

*Aktivität 1: Supermarkt-Rollenspiel*
- Setting: Therapieraum mit Regalen und Produkten
- Durchführung: Einkaufsliste abarbeiten, Produkte finden, Preise vergleichen, bezahlen
- Schwerpunkt: Orientierung, Planung, Handlungssequenzen, Kommunikation

*Aktivität 2: Online-Bestellung planen*
- Setting: Computer/Tablet
- Durchführung: Lebensmittel-Webshop erkunden, Warenkorb zusammenstellen, Bestellung simulieren
- Schwerpunkt: Digitale Kompetenz, Planung, Entscheidungsfindung

*Aktivität 3: Menüplanung mit Einkaufsliste*
- Setting: Tisch mit Rezepten und Stift
- Durchführung: Wochenmenü planen, Zutaten auflisten, Mengen berechnen
- Schwerpunkt: Planung, Kognition, Exekutivfunktionen

**Deine Aufgabe:**
Erstelle nach diesem Muster Aktivitätenpools für:
- Betätigung "Kochen"
- Betätigung "Sich anziehen"
- Betätigung "Körperpflege"
- Betätigung "Telefon nutzen"
- Betätigung "Post erledigen"

**Experimentiere:**
- Wie spezifisch sollten deine Beispiele sein?
- Was passiert, wenn du unterschiedliche Schwierigkeitsgrade in den Beispielen zeigst?
- Kannst du Schwerpunkte vorgeben? (z.B. "Fokus auf kognitive Aspekte")

**Beispiel-Prompt:**
"Erstelle nach dem Muster der drei Beispiele für 'Einkaufen' einen Pool von 5 therapeutischen Aktivitäten für die Betätigung 'Kochen'. Beschreibe jeweils Setting, Durchführung und therapeutischen Schwerpunkt."

✅ **Praxistauglich:** Baue dir einen Aktivitätenpool als Inspirationsquelle für die Therapieplanung!""",
            "hint": "💭 Ein breiter Aktivitätenpool gibt dir Flexibilität in der Therapiegestaltung.",
        }
    },
    "Chain-of-Thought Prompting": {
        "Aushang Leichte Sprache": {
            "task": """🎯 Lernziel: Entwickle Chain-of-Thought Prompts für komplexe Aufgaben

**Aufgabe:**
Erstelle einen Aushang in Leichter Sprache für eine WfbM.

**Inhalt:** Ankündigung der neuen "Morgensportrunde"
- Findet täglich um 9 Uhr statt
- Für alle Mitarbeiter:innen, die Lust haben
- Ziel: Aktiv in den Tag starten

**Identifiziere die notwendigen Denkschritte:**

Mögliche Struktur:
1. **Zielgruppenanalyse:** Wer soll den Aushang lesen? Welches Sprachniveau?
2. **Kernbotschaft:** Was ist die wichtigste Information?
3. **Informationsaufbereitung:** Welche Details sind wichtig? Welche weglassen?
4. **Sprachliche Umsetzung:** Wie formuliere ich in Leichter Sprache?
5. **Formatentscheidung:** Wie sieht der Aushang aus? Überschrift? Absätze? Symbole?

**Experimentiere mit der Prompt-Struktur:**
- Gibst du alle Schritte vor oder lässt du die KI selbst strukturieren?
- Wie detailliert müssen die Zwischenschritte sein?
- Was passiert, wenn du die KI bittest, ihre Gedanken zu zeigen?

**Beispiel-Prompt:**
"Erstelle einen Aushang für die WfbM über die neue Morgensportrunde (täglich 9 Uhr, für alle). Gehe dabei schrittweise vor:
1. Analysiere die Zielgruppe und ihr Sprachniveau
2. Identifiziere die Kernbotschaft
3. Wähle die wichtigen Informationen aus
4. Formuliere in Leichter Sprache mit kurzen Sätzen
5. Strukturiere den Aushang übersichtlich

Zeige jeden Denkschritt."

✅ **Praxistauglich:** So erstellst du barrierefreie Informationen für verschiedene Settings!""",
            "hint": "💭 Die Aufteilung in Denkschritte hilft der KI, systematisch und nichts zu vergessen. Du kannst die Schritte auch selbst durchdenken und nur die Umsetzung von der KI machen lassen.",
        },
        "Hilfsmittel recherchieren": {
            "task": """🎯 Lernziel: Nutze Chain-of-Thought für strukturierte Recherche

**Aufgabe:**
Recherchiere Hilfsmittel für eine bestimmte Betätigung - generisch, ohne konkrete Klient:in!

**Beispiel-Betätigung:** "Essen mit Besteck"

**Entwickle einen Prompt mit folgenden Denkschritten:**

1. **Betätigung analysieren**
   - Was gehört alles dazu?
   - Welche Teilschritte gibt es?
   - Was könnte schwierig sein?

2. **Häufige Einschränkungen identifizieren**
   - Welche funktionellen Einschränkungen beeinträchtigen diese Betätigung typischerweise?
   - (z.B. bei "Essen mit Besteck": Greifkraft, Beweglichkeit, Koordination, Tremor)

3. **Hilfsmittelkategorien bestimmen**
   - Welche Kategorien von Hilfsmitteln gibt es?
   - (z.B. Besteck-Adaptionen, Teller-Adaptionen, Unterlagen)

4. **Konkrete Hilfsmittel recherchieren**
   - Welche spezifischen Hilfsmittel gibt es pro Kategorie?
   - Für welche Einschränkung ist welches geeignet?

5. **Übersichtlich strukturieren**
   - Erstelle eine Übersicht nach Einschränkungen oder nach Hilfsmitteltypen

**Weitere Betätigungen zum Üben:**
- Anziehen (Oberkörper)
- Körperpflege (Haare kämmen, Zähne putzen)
- Schreiben
- Telefonieren (Festnetz/Handy)
- Türen öffnen

**Experimentiere:**
- Wie explizit müssen die Schritte sein?
- Kannst du Schritte zusammenfassen?
- Was passiert, wenn du die KI bittest, selbst Schritte zu entwickeln?

**Beispiel-Prompt:**
"Recherchiere Hilfsmittel für die Betätigung 'Essen mit Besteck'. Gehe dabei systematisch vor:
1. Analysiere die Betätigung und ihre Teilschritte
2. Identifiziere häufige Einschränkungen, die diese Betätigung erschweren
3. Bestimme Kategorien von Hilfsmitteln
4. Recherchiere konkrete Hilfsmittel pro Kategorie
5. Erstelle eine strukturierte Übersicht

Zeige deine Denkschritte."

✅ **Praxistauglich:** Diese Recherchen helfen dir, dein Hilfsmittelwissen aufzubauen!""",
            "hint": "💭 Strukturierte Recherche ist effizienter als unsystematisches Suchen. Die KI kann dir helfen, systematisch vorzugehen.",
        },
        "Literatur erschließen": {
            "task": """🎯 Lernziel: Nutze Chain-of-Thought für Literaturarbeit

**Aufgabe:**
Erschließe einen Fachartikel oder ein Buchkapitel strukturiert.

**Beispiel:** Du hast einen wissenschaftlichen Artikel zu einem therapeutischen Ansatz und möchtest ihn für die Praxis aufbereiten.

**Entwickle einen Prompt mit folgenden Denkschritten:**

1. **Überblick verschaffen**
   - Worum geht es grundsätzlich?
   - Was ist die Hauptaussage/These?

2. **Theoretischen Hintergrund erfassen**
   - Auf welcher Theorie/welchem Konzept basiert der Ansatz?
   - Welche Grundannahmen werden gemacht?

3. **Praktische Anwendung verstehen**
   - Wie wird der Ansatz konkret angewendet?
   - Welche Schritte/Methoden werden beschrieben?

4. **Evidenz bewerten**
   - Welche Studien/Belege werden genannt?
   - Wie stark ist die Evidenz?

5. **Praxisrelevanz einschätzen**
   - Für welche Klient:innen/Settings ist das relevant?
   - Was kann ich direkt umsetzen?
   - Was muss ich beachten?

6. **Zusammenfassung erstellen**
   - Fasse die Kernpunkte in 3-5 Sätzen zusammen

**Anwendungsbeispiele:**
- CO-OP Ansatz (Cognitive Orientation to daily Occupational Performance)
- Affolter-Modell
- CMOP-E (Canadian Model of Occupational Performance and Engagement)
- Sensorische Integrationstherapie
- Perfetti-Konzept

**Experimentiere:**
- Kannst du den Original-Text in den Prompt einfügen? (bei kürzeren Texten)
- Oder gibst du nur das Thema vor und die KI recherchiert selbst?
- Wie detailliert sollen die einzelnen Schritte sein?

**Beispiel-Prompt:**
"Erschließe mir den CO-OP Ansatz strukturiert. Gehe dabei vor in folgenden Schritten:
1. Überblick: Was ist CO-OP?
2. Theoretischer Hintergrund: Auf welcher Grundlage basiert CO-OP?
3. Praktische Anwendung: Wie wird CO-OP konkret durchgeführt?
4. Evidenz: Welche Belege gibt es für die Wirksamkeit?
5. Praxisrelevanz: Für wen ist CO-OP geeignet? Was muss ich beachten?
6. Zusammenfassung in 5 Sätzen

Zeige jeden Schritt klar."

✅ **Praxistauglich:** So erschließt du dir neue Therapiekonzepte systematisch!""",
            "hint": "💭 Systematische Literaturarbeit spart Zeit und hilft dir, neue Konzepte schnell zu verstehen und zu bewerten.",
        }
    },
    "Skala Prompting": {
        "Was ist Betätigung?": {
            "task": """🎯 Lernziel: Entwickle Skala-Prompts für verschiedene Sprachniveaus

**Aufgabe:**
Bereite die DVE-Definition von "Betätigung" für verschiedene Zielgruppen auf.

**Die Original-Definition:**
"Unter Betätigung verstehen Ergotherapeuten die Summe von Aktivitäten und Aufgaben des täglichen Lebens, die durch Individuen und Kultur benannt, strukturiert und mit Bedeutung versehen sind. Betätigungen werden individuell unterschiedlich ausgeführt, sind Ausdruck unserer Persönlichkeit und lassen uns fortlaufend mit unserer Umwelt interagieren. Betätigung gehört zu den Grundbedürfnissen des Menschen und umfasst alles, was Menschen tun. Dazu gehören Tätigkeiten zur Versorgung der eigenen Person (Selbstversorgung), zum Genuss des Lebens (Freizeit) und als Beitrag zur sozialen und ökonomischen Entwicklung des Individuums und der Gemeinschaft (Produktivität). Bedeutungsvolle Aktivitäten sind für den Menschen dadurch charakterisiert, dass sie zielgerichtet sind und als signifikant, sinnvoll und wertvoll für den Einzelnen empfunden werden."

(Quelle: Kohlhuber, Ergotherapie - betätigungszentriert in Ausbildung und Praxis, 2020)

**Definiere deine Skala:**

Klassische Variante:
- Stufe 1 = Alltagssprache, sehr einfach
- Stufe 10 = Wissenschaftliche Fachsprache, komplex

Alternative Varianten:
- Stufe 1 = Leichte Sprache, Stufe 10 = Fachsprache für Expert:innen
- Stufe 1 = Jugendsprache/TikTok, Stufe 10 = Elaborierte Fachsprache
- Stufe 1 = Für Kinder erklärt, Stufe 10 = Für Fachpublikation

**Experimentiere:**
1. Lass die KI zunächst die Original-Definition einsortieren
2. Verschiebe die Definition auf der Skala (z.B. auf Stufe 3 oder Stufe 8)
3. Probiere verschiedene Skalenendpunkte aus
4. Was passiert, wenn du Zwischenstufen definierst?

**Beispiel-Prompt:**
"Hier ist eine Definition von Betätigung: [Definition einfügen]

Erstelle eine Skala von 1-10, wobei:
- Stufe 1 = Alltagssprache, verständlich für alle
- Stufe 10 = Wissenschaftliche Fachsprache

Sortiere die Definition ein und erstelle dann eine Version auf Stufe 3 (einfache, aber korrekte Sprache für Klient:innen)."

✅ **Praxistauglich:** So bereitest du Fachinhalte für unterschiedliche Zielgruppen auf!""",
            "hint": "💭 Die gleiche Information kann auf verschiedenen Sprachniveaus unterschiedlich wirken. Welches Niveau passt zu welcher Zielgruppe?",
        },
        "Was ist Ergotherapie?": {
            "task": """🎯 Lernziel: Passe Komplexität gezielt an verschiedene Zielgruppen an

**Aufgabe:**
Erkläre "Was ist Ergotherapie?" für verschiedene Zielgruppen.

**Die DVE-Definition:**
"Ergotherapie unterstützt und begleitet Menschen jeden Alters, die in ihrer Handlungsfähigkeit eingeschränkt oder von Einschränkung bedroht sind. Ziel ist, sie bei der Durchführung für sie bedeutungsvoller Betätigungen in den Bereichen Selbstversorgung, Produktivität und Freizeit in ihrer persönlichen Umwelt zu stärken. Hierbei dienen spezifische Aktivitäten, Umweltanpassung und Beratung dazu, dem Menschen Handlungsfähigkeit im Alltag, gesellschaftliche Teilhabe und eine Verbesserung seiner Lebensqualität zu ermöglichen."

(Quelle: https://dve.info/ergotherapie/definition)

**Mögliche Zielgruppen und Sprachniveaus:**

- **Stufe 2-3:** Für Kindergartenkinder
- **Stufe 4-5:** Für Patient:innen ohne Vorerfahrung
- **Stufe 6-7:** Für Angehörige / interessierte Laien
- **Stufe 8-9:** Für medizinisches Fachpersonal (Ärzt:innen, Pflege)
- **Stufe 10:** Für ergotherapeutische Fachpublikation

**Experimentiere:**
- Wie verändert sich die Definition auf verschiedenen Stufen?
- Welche Aspekte bleiben gleich, welche werden vereinfacht/komplexer?
- Probiere ungewöhnliche Endpunkte aus (z.B. "in Reimform" vs. "wissenschaftlich")

**Beispiel-Prompt:**
"Hier ist die DVE-Definition von Ergotherapie: [Definition einfügen]

Erstelle eine Skala:
- Stufe 1 = Für 5-Jährige erklärbar
- Stufe 10 = Wissenschaftliche Fachpublikation

Wo würdest du die aktuelle Definition einsortieren? Erstelle dann eine Version auf Stufe 4 (für neue Patient:innen in der Ergotherapie)."

✅ **Praxistauglich:** Diese Erklärungen kannst du für Flyer, Webseite, Beratungen nutzen!""",
            "hint": "💭 Die Fähigkeit, Fachkonzepte auf verschiedenen Niveaus zu erklären, ist eine Kernkompetenz in der therapeutischen Kommunikation.",
        }
    },
    "Role Prompting": {
        "Ethisches Dilemma reflektieren": {
            "task": """🎯 Lernziel: Nutze Role Prompting für ethische Reflexion

**Aufgabe:**
Reflektiere ein ethisches Dilemma aus verschiedenen Perspektiven - ohne konkreten Fall!

**Beispiel-Dilemma:**
"Eine Person mit beginnender Demenz möchte weiterhin alleine Auto fahren. Die Angehörigen sind besorgt um die Sicherheit. Die Person selbst sagt, das Auto sei ihre Freiheit und ohne Auto fühle sie sich eingesperrt."

**Kernkonflikt:** Autonomie vs. Sicherheit

**Perspektiven, die du einnehmen lassen kannst:**

1. **Rolle: Die betroffene Person**
   - Wie erlebt sie die Situation?
   - Was bedeutet Autofahren für sie?
   - Wie nimmt sie die Sorgen wahr?

2. **Rolle: Angehörige/Partner:in**
   - Welche Ängste und Sorgen bestehen?
   - Was ist ihre Verantwortung?
   - Wie könnten sie unterstützen?

3. **Rolle: Ergotherapeut:in**
   - Welche professionelle Haltung ist angemessen?
   - Wie moderiere ich zwischen Autonomie und Sicherheit?
   - Welche betätigungsorientierten Lösungen gibt es?

4. **Rolle: Ethiker:in / neutrale:r Beobachter:in**
   - Welche ethischen Prinzipien sind berührt?
   - Wie gewichtet man Autonomie vs. Sicherheit?
   - Was wäre ein fairer Kompromiss?

**Weitere Dilemmata zum Üben:**
- Sturzgefahr vs. Bewegungsfreiheit bei Senior:innen
- Medikamentenmanagement: Selbstständigkeit vs. korrekte Einnahme
- Arbeitsplatzgestaltung: Leistungsfähigkeit vs. gesundheitliche Grenzen
- Kindeswohl: Förderung vs. Überforderung
- Digitale Medien: Teilhabe vs. Überstimulation

**Experimentiere:**
- Wie detailliert muss die Rollenbeschreibung sein?
- Kannst du die KI bitten, zwischen den Rollen zu wechseln?
- Was passiert, wenn du nach Gemeinsamkeiten der Perspektiven fragst?

**Beispiel-Prompt:**
"Betrachte folgendes ethisches Dilemma: [Dilemma beschreiben]

Nimm nacheinander vier Perspektiven ein:
1. Die betroffene Person selbst
2. Ein/e Angehörige/r
3. Eine/n Ergotherapeut:in mit betätigungsorientierter Haltung
4. Eine/n Ethiker:in

Beschreibe aus jeder Perspektive: Was ist wichtig? Was wird befürchtet? Was wäre eine Lösung?

Analysiere am Ende: Wo gibt es Gemeinsamkeiten? Wo unauflösbare Konflikte?"

✅ **Praxistauglich:** Ethische Reflexion hilft dir, in schwierigen Situationen verschiedene Perspektiven zu würdigen!""",
            "hint": "💭 Das Einnehmen verschiedener Perspektiven schärft dein ethisches Urteilsvermögen und deine Empathie.",
        },
        "Betätigungskonflikt aus verschiedenen Blickwinkeln": {
            "task": """🎯 Lernziel: Nutze Role Prompting für therapeutische Reflexion

**Aufgabe:**
Betrachte einen Betätigungskonflikt aus verschiedenen therapeutischen Blickwinkeln - generisch!

**Beispiel-Situation:**
"Eine Person möchte wieder arbeiten gehen nach längerer Krankheit. Die Ärzt:innen empfehlen eine Reduktion der Arbeitszeit. Die Person selbst möchte aber Vollzeit arbeiten, weil sie sich sonst 'als halber Mensch' fühlt."

**Perspektiven:**

1. **Rolle: Funktionsorientierte:r Therapeut:in**
   - Fokus auf körperliche Belastbarkeit
   - Was sagen die medizinischen Befunde?
   - Welche Funktionen müssen trainiert werden?

2. **Rolle: Betätigungsorientierte:r Therapeut:in**
   - Fokus auf bedeutungsvolle Betätigung "Arbeiten"
   - Was bedeutet Arbeit für die Person?
   - Wie kann die Betätigung ermöglicht werden? (Nicht: Wie trainiere ich Funktionen)
   - Welche Anpassungen sind möglich?

3. **Rolle: Systemische:r Therapeut:in**
   - Fokus auf das gesamte System (Familie, Arbeitgeber, soziales Umfeld)
   - Welche Faktoren beeinflussen die Situation?
   - Wer ist alles betroffen?
   - Welche Lösungen berücksichtigen alle Beteiligten?

4. **Rolle: Klient:innenzentrierte:r Therapeut:in**
   - Fokus auf die Ziele und Werte der Person
   - Was ist der Person wichtig?
   - Wie kann ich die Person in ihrer Entscheidung unterstützen?
   - Welche Ressourcen hat die Person?

**Weitere Situationen zum Üben:**
- Person möchte alleine leben, Angehörige sehen das kritisch
- Kind möchte wie alle anderen sein, braucht aber Unterstützung
- Person möchte Auto fahren trotz Einschränkungen
- Person möchte Hobby fortsetzen, das körperlich belastend ist

**Experimentiere:**
- Beschreibe die Haltungen der verschiedenen therapeutischen Ansätze
- Lass die KI die Unterschiede herausarbeiten
- Frage nach einer integrativen Perspektive

**Beispiel-Prompt:**
"Betrachte folgende Situation: [Situation beschreiben]

Analysiere sie aus vier therapeutischen Perspektiven:

1. Funktionsorientierte Ergotherapie (Fokus: Funktionen trainieren)
2. Betätigungsorientierte Ergotherapie (Fokus: Betätigung ermöglichen)
3. Systemische Perspektive (Fokus: gesamtes System)
4. Klient:innenzentrierte Perspektive (Fokus: Ziele der Person)

Was würde jeder Ansatz betonen? Wo sind die Unterschiede? Welche Perspektive erscheint dir am hilfreichsten?"

✅ **Praxistauglich:** Diese Reflexion hilft dir, deinen eigenen therapeutischen Ansatz zu schärfen!""",
            "hint": "💭 Verschiedene therapeutische Ansätze haben unterschiedliche Stärken. Role Prompting hilft dir, diese zu verstehen.",
        }
    },
    "Constraint Prompting": {
        "Fachliteratur kompakt zusammenfassen": {
            "task": """🎯 Lernziel: Nutze Constraints für prägnante Zusammenfassungen

**Aufgabe:**
Fasse Fachliteratur unter strengen Längenvorgaben zusammen.

**Beispiel-Material:**
Ein wissenschaftlicher Artikel über einen therapeutischen Ansatz, eine Studie, ein Buchkapitel

**Experimentiere mit verschiedenen Constraints:**

**Constraint 1: Länge**
- "Maximal 100 Wörter"
- "Genau 3 Sätze"
- "Maximal 500 Zeichen (für Social Media)"
- "Ein Tweet (280 Zeichen)"

**Constraint 2: Inhaltlicher Fokus**
- "Nur die Kernaussage"
- "Nur die praktische Anwendung, keine Theorie"
- "Nur die Evidenz / Studienlage"
- "Nur das, was direkt umsetzbar ist"

**Constraint 3: Zielgruppe**
- "Für Kolleg:innen"
- "Für interessierte Laien"
- "Für eine Teambesprechung (2 Minuten Redezeit)"

**Kombiniere mehrere Constraints:**
- "Maximal 100 Wörter + Fokus auf praktische Anwendung + für Kolleg:innen"
- "Genau 3 Sätze + nur Kernaussage + für Teambesprechung"

**Themen zum Üben:**
- CO-OP Ansatz
- Sensorische Integrationstherapie
- CMOP-E Modell
- Evidenz für Ergotherapie bei Schlaganfall
- Betätigungsorientierung vs. Funktionsorientierung

**Beispiel-Prompt (einfach):**
"Fasse den CO-OP Ansatz in maximal 100 Wörtern zusammen."

**Beispiel-Prompt (komplex):**
"Fasse den CO-OP Ansatz zusammen. Constraints:
- Maximal 100 Wörter
- Fokus NUR auf die praktische Anwendung (keine Theorie)
- Für eine Teambesprechung mit Kolleg:innen
- Erkläre es so, dass jemand es direkt ausprobieren könnte"

✅ **Praxistauglich:** Kompakte Zusammenfassungen brauchst du für Teambesprechungen, Dokumentation, Fortbildungen!""",
            "hint": "💭 Je mehr Constraints du setzt, desto fokussierter wird das Ergebnis. Aber: Zu viele Constraints können auch zu restriktiv sein!",
        },
        "Komplexe Konzepte vereinfachen": {
            "task": """🎯 Lernziel: Nutze Constraints für zielgruppengerechte Erklärungen

**Aufgabe:**
Erkläre komplexe ergotherapeutische Konzepte für verschiedene Zielgruppen unter Einhaltung strenger Vorgaben.

**Beispiel-Konzept:**
"Betätigungsorientierung" - ein Kernkonzept der Ergotherapie, aber schwer zu erklären!

**Constraint-Typen die du kombinieren kannst:**

**Sprachliche Constraints:**
- "Keine Fachbegriffe"
- "Nur einfache Hauptsätze, keine Nebensätze"
- "Keine Fremdwörter"
- "Keine Passiv-Konstruktionen"
- "Nur Wörter, die ein 10-Jähriger kennt"

**Strukturelle Constraints:**
- "Maximal 5 Sätze"
- "Mit einem konkreten Beispiel"
- "Als Frage und Antwort"
- "Als Geschichte"

**Inhaltliche Constraints:**
- "Ohne Theorie, nur praktisch"
- "Ohne Negationen (nicht sagen was es NICHT ist)"
- "Mit Alltagsbeispielen"

**Tonale Constraints:**
- "Ermutigend, nicht belehrend"
- "Neutral, sachlich"
- "Warm, empathisch"

**Konzepte zum Üben:**
- Betätigungsorientierung
- Klientenzentrierung
- Umweltanpassung vs. Personentraining
- Top-down vs. Bottom-up Ansatz
- Betätigungsperformanz

**Zielgruppen:**
- Für neue Klient:innen (ersten Termin)
- Für Angehörige
- Für Ärzt:innen (die Ergotherapie verordnen)
- Für Kinder (8-12 Jahre)
- Für Menschen mit kognitiven Einschränkungen

**Beispiel-Prompt (einfach):**
"Erkläre 'Betätigungsorientierung' in maximal 5 Sätzen ohne Fachbegriffe."

**Beispiel-Prompt (komplex):**
"Erkläre 'Betätigungsorientierung' für neue Klient:innen. Constraints:
- Maximal 5 Sätze
- Keine Fachbegriffe oder Fremdwörter
- Mit einem konkreten Alltagsbeispiel
- Ermutigend, nicht belehrend
- Erkläre, WARUM das wichtig ist (nicht nur WAS es ist)"

✅ **Praxistauglich:** Diese Erklärungen brauchst du täglich in der Beratung und Aufklärung!""",
            "hint": "💭 Die Fähigkeit, komplexe Konzepte einfach zu erklären, zeigt, dass du sie wirklich verstanden hast!",
        }
    }
}

technique_intros = {
    "Zero-Shot Prompting": {
        "title": "Zero-Shot Prompting 🎯",
        "description": """**Eine klare Anweisung, ohne Beispiele.**

Du sagst der KI direkt, was du möchtest - präzise und strukturiert. Je klarer deine Anweisung, desto besser das Ergebnis.

**Wann nutzen?** Für standardisierte Materialien, klare Aufgaben, strukturierte Inhalte."""
    },
    "One-Shot Prompting": {
        "title": "One-Shot Prompting 📝",
        "description": """**Ein Beispiel als Schablone.**

Du zeigst der KI einmal, wie das Ergebnis aussehen soll. Sie nutzt dieses Muster für weitere Aufgaben.

**Wann nutzen?** Für einheitliche Formate, Serien von Materialien, konsistente Strukturen."""
    },
    "Few-Shot Prompting": {
        "title": "Few-Shot Prompting 🎯🎯🎯",
        "description": """**Mehrere Beispiele etablieren ein Muster.**

Du gibst 2-5 Beispiele, aus denen die KI das Muster erkennt und auf neue Inhalte überträgt.

**Wann nutzen?** Für komplexere Transformationen, Analysen, kreative Aufgaben."""
    },
    "Chain-of-Thought Prompting": {
        "title": "Chain-of-Thought Prompting 🔄",
        "description": """**Schritt für Schritt zum Ziel.**

Du teilst komplexe Aufgaben in logische Denkschritte auf. Die KI arbeitet systematisch jeden Schritt ab.

**Wann nutzen?** Für komplexe Recherchen, Analysen, strukturierte Planungen."""
    },
    "Skala Prompting": {
        "title": "Skala Prompting 📊",
        "description": """**Inhalte gezielt anpassen.**

Du definierst eine Skala (z.B. Sprachniveau 1-10) und verschiebst Inhalte entlang dieser Skala.

**Wann nutzen?** Für verschiedene Zielgruppen, Sprachniveaus, Komplexitätsgrade."""
    },
    "Role Prompting": {
        "title": "Role Prompting 🎭",
        "description": """**Perspektivwechsel durch Rollen.**

Du weist der KI eine Rolle zu (z.B. "Du bist eine erfahrene Ergotherapeutin mit betätigungsorientierter Haltung"). Die KI nimmt diese Perspektive ein.

**Wann nutzen?** Für Reflexion, verschiedene Blickwinkel, ethische Dilemmata."""
    },
    "Constraint Prompting": {
        "title": "Constraint Prompting 🎯",
        "description": """**Klare Grenzen setzen.**

Du gibst der KI strikte Vorgaben (Länge, Stil, verbotene Begriffe, Struktur). Sie hält sich daran.

**Wann nutzen?** Für prägnante Texte, zielgruppengerechte Sprache, fokussierte Inhalte."""
    }
}

def display_task_with_hint(technique, exercise):
    """Zeigt Aufgabe mit optionalem Hint-Expander"""
    st.markdown(task_messages[technique][exercise]["task"])
    
    # Nur wenn explizit ein Hint vorhanden ist
    if "hint" in task_messages[technique][exercise]:
        with st.expander("💡 Tipp", expanded=False):
            st.markdown(task_messages[technique][exercise]["hint"])

def get_teacher_feedback(technique, exercise=None):
    """Generiert kontextspezifisches Feedback vom Teacher als strukturiertes JSON"""
    import json
    import time

    current_task = task_messages[technique]
    if isinstance(current_task, dict):
        current_task = current_task[exercise]["task"] if exercise else current_task["task"]

    teacher_prompt = f"""Gib mir ein strukturiertes Feedback zu folgender Übung.

WICHTIG: Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt. Kein zusätzlicher Text davor oder danach!

Aktuelle Technik: {technique}
Aktuelle Aufgabe: {current_task}

Setze in deinem Feedback den Fokus hauptsächlich auf meinen letzten Promptingversuch. Wenn es für meinen Lernerfolg sinnvoll ist, beziehe aber auch Unterschiede, Verbesserungen oder Verschlechterungen zu vorherigen Versuchen in den Blick. Tue dies aber nur, wenn es didaktisch zielführend ist.

Gesprächsverlauf:
{str(st.session_state.displayed_messages)}

Antworte mit folgendem JSON-Format:
{{
    "gesamtbewertung": "Eine kurze Zusammenfassung (1-2 Sätze)",
    "staerken": [
        "Stärke 1",
        "Stärke 2"
    ],
    "verbesserungspotenzial": [
        "Verbesserungsvorschlag 1",
        "Verbesserungsvorschlag 2"
    ],
    "konkrete_tipps": [
        "Konkreter Tipp 1",
        "Konkreter Tipp 2"
    ],
    "beispiel_prompt": "Ein verbesserter Beispiel-Prompt (optional)"
}}

Antworte NUR mit dem JSON-Objekt, ohne Markdown-Formatierung oder zusätzlichen Text!"""

    teacher_messages = [
        {"role": "system", "content": st.session_state.teacher_sys_prompt},
        {"role": "user", "content": teacher_prompt}
    ]

    # Versuche bis zu 2x bei Fehlern
    for attempt in range(2):
        try:
            feedback_raw = llm_provider.call_llm(
                model=st.session_state.teacher_model if attempt == 0 else st.session_state.teacher_model_if_error,
                temperature=st.session_state.teacher_temp,
                messages=teacher_messages
            )

            # Versuche JSON zu parsen
            # Entferne mögliche Markdown-Code-Blöcke
            feedback_clean = feedback_raw.strip()
            if feedback_clean.startswith("```json"):
                feedback_clean = feedback_clean[7:]
            if feedback_clean.startswith("```"):
                feedback_clean = feedback_clean[3:]
            if feedback_clean.endswith("```"):
                feedback_clean = feedback_clean[:-3]
            feedback_clean = feedback_clean.strip()

            feedback_json = json.loads(feedback_clean)

            # Speichere strukturiertes Feedback
            st.session_state.teacher_messages.append({
                "role": "assistant",
                "content": feedback_json
            })

            return feedback_json

        except json.JSONDecodeError:
            # Bei JSON-Fehler: Warte kurz und versuche es mit Fallback-Modell
            if attempt == 0:
                time.sleep(2)
                continue
            else:
                # Beim zweiten Fehlschlag: Gib Fehler zurück
                return {
                    "gesamtbewertung": "Fehler beim Generieren des Feedbacks. Bitte versuche es erneut.",
                    "staerken": [],
                    "verbesserungspotenzial": [],
                    "konkrete_tipps": ["Klicke erneut auf 'Feedback holen'"],
                    "beispiel_prompt": None
                }
        except Exception as e:
            # Bei anderen Fehlern: Warte und retry
            if attempt == 0:
                time.sleep(2)
                continue
            else:
                return {
                    "gesamtbewertung": f"Fehler: {str(e)}. Bitte versuche es erneut.",
                    "staerken": [],
                    "verbesserungspotenzial": [],
                    "konkrete_tipps": ["Klicke erneut auf 'Feedback holen'"],
                    "beispiel_prompt": None
                }

# Seitenleiste - Clean und fokussiert
with st.sidebar:
    st.header("🎯 Wähle eine Technik")
            
    technique = st.selectbox(
        "Prompting-Technik:",
        ["Zero-Shot Prompting",
         "One-Shot Prompting",
         "Few-Shot Prompting",
         "Chain-of-Thought Prompting",
         "Skala Prompting",
         "Role Prompting",
         "Constraint Prompting"],
        label_visibility="collapsed"
    )

    if technique == "Zero-Shot Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Informationsblatt Ergonomie",
             "Traumreise",
             "Beratungskonzept strukturieren"]
        )
    elif technique == "One-Shot Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Übungsanleitung erstellen",
             "Infomaterial-Serie"]
        )
    elif technique == "Few-Shot Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Betätigungsanalyse",
             "Aktivitätenpool erstellen"]
        )
    elif technique == "Chain-of-Thought Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Aushang Leichte Sprache",
             "Hilfsmittel recherchieren",
             "Literatur erschließen"]
        )
    elif technique == "Skala Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Was ist Betätigung?",
             "Was ist Ergotherapie?"]
        )
    elif technique == "Role Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Ethisches Dilemma reflektieren",
             "Betätigungskonflikt aus verschiedenen Blickwinkeln"]
        )
    elif technique == "Constraint Prompting":
        exercise = st.selectbox(
            "Übung:",
            ["Fachliteratur kompakt zusammenfassen",
             "Komplexe Konzepte vereinfachen"]
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓ Los geht's", use_container_width=True):
            st.session_state.messages = [
                {"role": "system", "content": st.session_state.sop_sys_prompt}]

            st.session_state.current_technique = technique
            st.session_state.current_exercise = exercise

            st.session_state.displayed_messages = []

            chat_ui.show_success_message(f"Starte {technique}!")

    with col2:
        if st.button("🔄 Neu", use_container_width=True):
            st.session_state.messages = [
                {"role": "system", "content": st.session_state.sop_sys_prompt}]

            st.session_state.current_technique = technique
            st.session_state.current_exercise = exercise

            st.session_state.displayed_messages = []
            chat_ui.show_success_message("Neustart!")

    st.markdown("---")
        
    def display_teacher_feedback(feedback):
        """Zeigt strukturiertes Teacher-Feedback responsiv an"""
        if isinstance(feedback, dict):
            # Gesamtbewertung
            st.markdown("### 📊 Gesamtbewertung")
            st.info(feedback.get("gesamtbewertung", "Keine Bewertung vorhanden"))

            col1, col2 = st.columns(2)

            # Stärken
            with col1:
                st.markdown("### ✅ Stärken")
                staerken = feedback.get("staerken", [])
                if staerken:
                    for staerke in staerken:
                        st.success(f"• {staerke}")
                else:
                    st.caption("Keine Stärken identifiziert")

            # Verbesserungspotenzial
            with col2:
                st.markdown("### 🎯 Verbesserungspotenzial")
                verbesserungen = feedback.get("verbesserungspotenzial", [])
                if verbesserungen:
                    for verb in verbesserungen:
                        st.warning(f"• {verb}")
                else:
                    st.caption("Keine Verbesserungen nötig")

            # Konkrete Tipps
            st.markdown("### 💡 Konkrete Tipps")
            tipps = feedback.get("konkrete_tipps", [])
            if tipps:
                for idx, tipp in enumerate(tipps, 1):
                    st.markdown(f"**{idx}.** {tipp}")
            else:
                st.caption("Keine Tipps vorhanden")

            # Beispiel-Prompt (optional)
            if feedback.get("beispiel_prompt"):
                st.markdown("### 📝 Beispiel-Prompt")
                st.code(feedback["beispiel_prompt"], language=None)
        else:
            # Fallback für Nicht-JSON-Feedback
            st.markdown(str(feedback))

    @st.dialog("🎓 Teacher", width="large")
    def teacher():
        if st.button("💡 Feedback holen", help="Lass dir Tipps geben", use_container_width=True):
            with st.spinner("🎓 Teacher analysiert..."):
                feedback = get_teacher_feedback(technique, exercise)
                display_teacher_feedback(feedback)

        with st.expander("📚 Bisheriges Feedback", False):
            if st.session_state.teacher_messages:
                for idx, msg in enumerate(st.session_state.teacher_messages):
                    st.markdown(f"#### Feedback #{idx+1}")
                    display_teacher_feedback(msg["content"])
                    if idx < len(st.session_state.teacher_messages) - 1:
                        st.markdown("---")
            else:
                st.info("Noch kein Feedback vorhanden.")

    if st.button("🎓 Teacher", use_container_width=True):
        teacher()

    st.markdown("---")

    # Erweiterte Einstellungen (Modelle & Systemprompt)
    with st.expander("⚙️ Erweiterte Einstellungen", expanded=False):
        st.info("ℹ️ **Hinweis:** Alle Änderungen gelten nur für diese Session. Die Datenbank wird nicht verändert.")

        # Tab-Navigation für bessere Übersicht
        tab1, tab2 = st.tabs(["🤖 Modelle", "📝 Systemprompt"])

        with tab1:
            st.markdown("#### Modell-Auswahl")
            st.info("💡 **Empfohlen:** Haiku 4.5 für Übungen (schnell & günstig), Sonnet 4.5 für Teacher (besseres Feedback)")

            # Verfügbare Modelle
            available_models = [
                "claude-haiku-4-5-20251001",
                "claude-sonnet-4-5-20250929",
                "claude-3-5-haiku-20241022",
                "gpt-4.1",
                "gpt-4.1-mini",
                "gpt-4.1-nano",
                "gpt-4o",
                "gpt-4o-mini"
            ]

            # Modell für Assistent (Übungen)
            st.markdown("**Assistent (für Übungen):**")

            # Finde den aktuellen Index für sop_model
            try:
                current_sop_index = available_models.index(st.session_state.sop_model)
            except ValueError:
                current_sop_index = 0

            new_sop_model = st.selectbox(
                "Hauptmodell:",
                available_models,
                index=current_sop_index,
                key="select_sop_model"
            )

            # Finde den aktuellen Index für sop_model_if_error
            try:
                current_sop_error_index = available_models.index(st.session_state.sop_model_if_error)
            except ValueError:
                current_sop_error_index = 1

            new_sop_model_if_error = st.selectbox(
                "Fallback-Modell:",
                available_models,
                index=current_sop_error_index,
                key="select_sop_model_if_error"
            )

            st.markdown("---")

            # Modell für Teacher
            st.markdown("**Teacher (für Feedback):**")

            # Finde den aktuellen Index für teacher_model
            try:
                current_teacher_index = available_models.index(st.session_state.teacher_model)
            except ValueError:
                current_teacher_index = 1

            new_teacher_model = st.selectbox(
                "Hauptmodell:",
                available_models,
                index=current_teacher_index,
                key="select_teacher_model"
            )

            # Finde den aktuellen Index für teacher_model_if_error
            try:
                current_teacher_error_index = available_models.index(st.session_state.teacher_model_if_error)
            except ValueError:
                current_teacher_error_index = 0

            new_teacher_model_if_error = st.selectbox(
                "Fallback-Modell:",
                available_models,
                index=current_teacher_error_index,
                key="select_teacher_model_if_error"
            )

            # Zeige aktuell aktive Modelle
            st.markdown("---")
            st.markdown("**📋 Aktuell aktiv:**")
            st.caption(f"Assistent: {st.session_state.sop_model}")
            st.caption(f"Teacher: {st.session_state.teacher_model}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Speichern", use_container_width=True, key="save_models"):
                    st.session_state.sop_model = new_sop_model
                    st.session_state.sop_model_if_error = new_sop_model_if_error
                    st.session_state.teacher_model = new_teacher_model
                    st.session_state.teacher_model_if_error = new_teacher_model_if_error
                    st.success("✅ Modelle aktualisiert!")
                    st.rerun()

            with col2:
                if st.button("🔄 Zurücksetzen", use_container_width=True, key="reset_models"):
                    # Lade Original-Modelle aus der Datenbank
                    original_sop_bot = db.get_bot("Assistent")
                    original_teacher_bot = db.get_bot("Teacher")
                    st.session_state.sop_model = original_sop_bot["model"]
                    st.session_state.sop_model_if_error = original_sop_bot["model_if_error"]
                    st.session_state.teacher_model = original_teacher_bot["model"]
                    st.session_state.teacher_model_if_error = original_teacher_bot["model_if_error"]
                    st.success("✅ Auf Original zurückgesetzt!")
                    st.rerun()

        with tab2:
            st.markdown("#### Systemprompt anpassen")
            st.warning("⚠️ **Achtung:** Änderungen am Systemprompt können das Verhalten des Assistenten grundlegend verändern. Nur ändern, wenn du verstehst, was du tust!")

            st.info("💡 Der Systemprompt definiert die grundlegende Rolle und das Verhalten des Assistenten. Er wird bei jedem Gespräch als erste Nachricht gesendet.")

            # Aktuellen Systemprompt anzeigen und bearbeiten lassen
            new_sys_prompt = st.text_area(
                "Systemprompt:",
                value=st.session_state.sop_sys_prompt,
                height=200,
                help="Hier kannst du den Systemprompt anpassen. Änderungen gelten ab dem nächsten Chat-Neustart."
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Speichern", use_container_width=True, key="save_sysprompt"):
                    st.session_state.sop_sys_prompt = new_sys_prompt
                    # Aktualisiere auch die erste Nachricht in messages
                    st.session_state.messages[0] = {"role": "system", "content": new_sys_prompt}
                    st.success("✅ Systemprompt aktualisiert!")

            with col2:
                if st.button("🔄 Zurücksetzen", use_container_width=True, key="reset_sysprompt"):
                    # Lade den Original-Systemprompt aus der Datenbank
                    original_bot = db.get_bot("Assistent")
                    st.session_state.sop_sys_prompt = original_bot["sys_prompt"]
                    st.session_state.messages[0] = {"role": "system", "content": original_bot["sys_prompt"]}
                    st.success("✅ Auf Original zurückgesetzt!")
                    st.rerun()

def display_chat():
    """Display chat messages with modern styling"""
    chat_ui.display_modern_chat_messages(st.session_state.displayed_messages, show_system=False)

def process_input():
    """Process user input with modern UI feedback"""
    if prompt := chat_ui.create_chat_input_with_placeholder("Schreib deinen Prompt hier..."):
        st.session_state.displayed_messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar=chat_ui.get_avatar("user")):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=chat_ui.get_avatar("assistant")):
            with st.spinner("💭 Denke nach..."):
                try:
                    full_response = llm_provider.call_llm(
                        model=st.session_state.sop_model,
                        temperature=st.session_state.sop_temp,
                        messages=st.session_state.messages
                    )
                    st.markdown(full_response)
                except:
                    try:
                        st.info(f"⚠️ Wechsle zu Fallback-Modell: {st.session_state.sop_model_if_error}")
                        full_response = llm_provider.call_llm(
                            model=st.session_state.sop_model_if_error,
                            temperature=st.session_state.sop_temp,
                            messages=st.session_state.messages
                        )
                        st.markdown(full_response)
                    except Exception as e:
                        error_msg = f"Fehler: {str(e)}"
                        chat_ui.show_error_message(error_msg)
                        full_response = "Entschuldigung, es gab einen Fehler."
                        st.markdown(full_response)

        st.session_state.displayed_messages.append({"role": "assistant", "content": full_response})
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if "current_technique" in st.session_state and "current_exercise" in st.session_state:
    technique = st.session_state.current_technique
    exercise = st.session_state.current_exercise
    
    # Technik-Beschreibung - kurz und direkt
    st.markdown(f"## {technique_intros[technique]['title']}")
    st.markdown(technique_intros[technique]['description'])
    
    st.markdown("---")
    
    # Aufgabe - mit optionalem Hint
    st.markdown("### 🎯 Deine Aufgabe")
    display_task_with_hint(technique, exercise)

# Chat anzeigen
display_chat()
process_input()