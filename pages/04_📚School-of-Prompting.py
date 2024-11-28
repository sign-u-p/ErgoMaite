import streamlit as st
import openai
from openai import OpenAI
import db
import pw_check as pw
import parameters as par

 #Passwort checken
if pw.check_password() == False:
    st.stop()

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

st.markdown("> 📚 **School-of-Prompting**")

# Expander für Einführung und Überblick
with st.expander("**Was ist die School-of-Prompting?**", False):
    st.markdown(
        "Hier lernst du verschiedene Prompting-Techniken kennen und übst deren Anwendung an praxisrelevanten Beispielen. " \
        "Die Beispiele sind so gewählt, dass sie die therapeutische Kompetenz unterstützen ohne sie zu ersetzen. "\
        "Wir machen hier Trockenübungen, um den Horizont möglicher Anwendungsmöglichkeiten in der Praxis abzustecken.")

with st.expander("💡 Prompting-Techniken im Überblick", False):
    st.markdown("""
        Hier findest du eine kurze Übersicht über die verschiedenen Techniken. 
        Wähle in der Seitenleiste eine Technik aus, um mehr darüber zu lernen und sie zu üben.
        """)
    
    st.subheader("Zero-Shot Prompting")
    st.markdown("""
        Stell dir Zero-Shot Prompting wie eine direkte Ansage vor: Du sagst genau, was du brauchst - ohne Beispiele oder Umschweife. 
        Das ist super praktisch für die ganzen organisatorischen Aufgaben in deiner Praxis.
        """)
    
    st.subheader("One-Shot Prompting")
    st.markdown("""
        Bei One-Shot Prompting zeigst du einmal vor, wie etwas aussehen soll. Die KI nutzt dann genau diese Struktur für weitere Inhalte. 
        Das spart dir Zeit bei der Dokumentation und hilft, einen einheitlichen Standard zu entwickeln.
        """)
    
    st.subheader("Few-Shot Prompting")
    st.markdown("""
        Few-Shot Prompting funktioniert mit mehreren Beispielen. Du zeigst der KI verschiedene Varianten und sie erkennt das Muster dahinter. 
        Das ist besonders hilfreich, wenn du betätigungsorientierte Formulierungen entwickeln willst.
        """)
    
    st.subheader("Chain-of-Thought Prompting")
    st.markdown("""
        Chain-of-Thought Prompting zerlegt komplexe Aufgaben in einzelne Schritte. 
        Das hilft dir, systematisch an Aufgaben heranzugehen und nichts zu vergessen.
        """)
    
    st.subheader("Skala Prompting")
    st.markdown("""
        Mit Skala Prompting kannst du Texte gezielt anpassen - zum Beispiel von Fachsprache zu Alltagssprache. 
        Das ist praktisch, wenn du mit unterschiedlichen Menschen kommunizierst.
        """)

# Dictionary mit Aufgabenstellungen
task_messages = {
    "Zero-Shot Prompting": {
        "Informationsblatt Ergonomie": {
            "task": """🎯 Lernziel: Entwickle einen präzisen Zero-Shot Prompt für ein Ergonomie-Informationsblatt

⚡️ Ausgangssituation:
Du sollst für deine Praxis ein Informationsblatt zum Thema 'Ergonomie am Arbeitsplatz' erstellen. 

⚡️ Deine Herausforderung:
1. Überlege zunächst: Was macht einen guten Zero-Shot Prompt aus?
2. Welche Aspekte müssen im Informationsblatt behandelt werden?
3. Experimentiere mit verschiedenen Formulierungen - was passiert, wenn du...
   - die Länge spezifizierst?
   - die Zielgruppe definierst? (Versuch doch z.B. mal, das Infoblatt als Aushang in einer WfbM zu erstellen.)
   - den Sprachstil festlegst? (Zum Beispiel: \"Kurz und knapp\", \"Motivierend\", \"Anschaulich\",...)

⚡️ Starte mit einem ersten Prompt-Versuch und optimiere ihn Schritt für Schritt!""",
            "hint": "Tipp: Vergleiche die Ergebnisse deiner verschiedenen Prompts. Was macht den Unterschied?",
            "example": "Anstatt direkt die Lösung zu kopieren, probiere verschiedene Ansätze: 'Erstelle ein...' vs. 'Formuliere knapp...' vs. 'Fasse zusammen...'"
        },
        "Traumreise": {
            "task": """🎯 Lernziel: Entwickle einen strukturierten Zero-Shot Prompt zum erstellen einer Traumreise

⚡️ Ausgangssituation:
Als Einstieg in eine Gruppentherapie möchtest du gern eine kurze Traumreise bereit halten, falls du merkst, dass es der Gruppe schwer fällt an zu kommen.

⚡️ Deine Herausforderung:
1. Entscheide dich für eine Zielgruppe
2. Entscheide dich für das Thema deiner Traumreise
3. Experimentiere mit der Prompt-Struktur:
   - Was passiert bei einer offenen Anfrage?
   - Was bei einer stark strukturierten?
   - Wie wirkt sich die Reihenfolge der Anforderungen aus?

⚡️ Versuche mindestens drei verschiedene Prompt-Varianten!""",
            "hint": "Tipp: Dokumentiere deine verschiedenen Prompts und deren Ergebnisse. Was funktioniert besser?",
            "example": "Statt 'Erstelle eine Traumreise...' könntest du auch 'Lass uns eine Traumreise für...entwickeln' probieren"
        },
    },
    "One-Shot Prompting": {
        "Dokumentation": {
            "task": """🎯 Lernziel: Entwickle One-Shot Prompts für Dokumentation

⚡️ Ausgangssituation:
Du hast dir im Laufe deines Arbeitstages folgende schnelle Notizen gemacht:
Arbeitsnotiz 13.11.24

7:30 Hausbesuch Fr. Meier (89)
- Küchentraining
- Kaffeemaschine bedienen übt sie jetzt selbstständig
- Neue Einhandtechnik zum Brotschmieren klappt super
- Feinziel \"selbstständige Frühstückszubereitung\" zu 80\% erreicht

9:00 Praxis - Tim (6J)
- Graphomotorik-Training
- Stifthaltung verbessert sich langsam
- Schwierigkeiten beim Druck dosieren
- Mit Therapieknete gearbeitet -> macht ihm Spaß
- Feinziel "korrekte Stifthaltung" noch nicht erreicht, braucht mehr Zeit

10:15 Erwachsenen-Gruppe \"Leben mit Schlaganfall\"
- 6 Teilnehmer
- Alltagsaktivitäten geübt: Knöpfe, Reißverschlüsse
- Hr. Schmidt macht super Fortschritte
- Fr. Klein braucht noch viel Unterstützung
- Gruppendynamik sehr gut
- Feinziel \"selbstständiges An-/Ausziehen\" bei 4 von 6 erreicht

13:00 Emma (4J)
- Sensorische Integration
- Schaukeln und Balancieren
- Heute sehr ängstlich auf Rollbrett
- Trotzdem 5min durchgehalten!
- Feinziel \"Gleichgewichtsreaktion\" teilweise erreicht

14:30 Hausbesuch Hr. Wagner (75)
- Badezimmer-Training
- Neue Antirutschmatte getestet
- Transfer in Badewanne noch unsicher
- Ehefrau eingewiesen in Hilfestellung
- Feinziel \"sicherer Transfer\" noch in Arbeit

16:00 Leon (8J)
- Konzentrationstraining
- Memory gespielt - deutlich besser als letzte Woche!
- Arbeitsblätter 10min am Stück geschafft
- Feinziel \"Aufmerksamkeitsspanne 10min\" erreicht

Noch zu dokumentieren:
- Entwicklungsbericht Tim
- Therapieplan Fr. Klein anpassen
- Hilfsmittelantrag Hr. Wagner

⚡️ Für deine Dokumentation verwendest du seit neustem einen Bogen mit fester Struktur. Der Bogen sieht wie folgt aus:

THERAPIE-DOKUMENTATION

Datum:
Uhrzeit:
Setting: [Hausbesuch/Praxis/Gruppe]
Klient/in:
Alter:

THERAPIEEINHEIT
Hauptziel der Einheit:
Durchgeführte Aktivitäten:
- 
- 
- 

Beobachtungen:
- Allgemeine Verfassung:
- Motivation/Mitarbeit:
- Besonderheiten:

ZIELERREICHUNG
Feinziel 1:
Status:

Feinziel 2:
Status:

PLANUNG
Nächste Schritte:
Zu beachten:

ORGANISATORISCHES
Zu erledigen:

⚡️ Deine Herausforderung:
1. Entwickle einen Prompt, mit dem du deine Notizen in die oben skizzierte Form bringen kannst.
2. Experimentiere mit verschiedenen Prompt-Varianten:
   - Wie kannst du die Vorlage am besten einbinden?
   - Was passiert, wenn du Teile weglässt?
   - Wie spezifisch musst du die gewünschte Struktur vorgeben?

⚡️ Teste verschiedene Formulierungen und vergleiche die Ergebnisse!""",
            "hint": "Tipp: Achte darauf, wie die KI die Vorlage interpretiert und übernimmt",
            "example": "Versuche es mit unterschiedlichen Ankern: 'Basierend auf diesem Beispiel...' vs. 'Übertrage diese Struktur...' vs. 'Adaptiere diese Vorlage...'"
        },
        "Wochenplan": {
            "task": """🎯 Lernziel: Entwickle One-Shot Prompts für die Gestaltung eines Wochenplanes

⚡️ Ausgangssituation:
Eine Klientin hat Schwierigkeiten den Ablauf ihrer Woche im Blick zu haben. Sie hat aber wiederkehrende Ereignisse im Alltag, die sich sehr gut in Form eines Wochenplanes darstellen ließen. 
Sie kann zwar von Ihrer Woche berichten, die Termine dann aber auch zur richtigen Zeit wahrszunehmen, bereitet ihr Schwierigkeiten. 
Wir gehen für unsere Übung einmal davon aus, dass wir ein Transkript (also eine Abschrift) unseres Gespräches mit der Klientin haben:

"Montags, ja, das ist immer mein Physiotherapie-Tag. Ich habe da einen festen Termin um 9:30 Uhr. Das tut mir immer gut, so ein bisschen Bewegung am Anfang der Woche. Letzte Woche war ich allerdings nicht dort – meine Tochter hatte es leider erwischt und war krank. Also musste ich absagen. Ich konnte nicht einfach zu Hause bleiben, weil ich noch auf meinen Enkel aufpassen musste. Das war irgendwie so ein Chaos, weil der Kleine, der ist ja erst drei, aber schon ein richtiges Energiebündel. Du kannst dir das gar nicht vorstellen, wie der durch die Wohnung fegt, als wäre er auf einen permanenten Zuckerschock. Das war auch nicht einfach, weil meine Tochter wirklich flach lag, also habe ich dann schnell den Staubsauger rausgeholt, um ihn zu beschäftigen – "Guck mal, wie der Staubsauger die Krümel frisst!" hat bei ihm immer gut funktioniert.

Dienstags treffe ich mich immer mit Frau Schmidt, meiner Nachbarin. Die ist auch schon in Rente und wir sind so eine Art Team geworden. Wir fahren gemeinsam um 10:00 Uhr zum Supermarkt. Es ist wirklich praktisch, weil wir uns abwechseln, wer fährt, und dann gibt\’s immer einen kleinen Plausch, während wir die Regale durchstöbern. Manchmal erzählen wir uns auch von den neuesten Klatschgeschichten aus dem Viertel. Und weißt du, was mir aufgefallen ist? Diese Sonderangebote – man kann echt nicht widerstehen, die sind so verlockend! Da landet immer noch eine Packung von irgendwas im Wagen, auch wenn ich eigentlich gar nicht vorhatte, das zu kaufen. Aber ich habe das Gefühl, dass Frau Schmidt uns auch immer wieder in Versuchung führt. Sie sagt dann immer: „Ach, das ist doch jetzt im Angebot!“

Mittwochs dann, da freue ich mich wirklich drauf: Wassergymnastik! Das ist um 15:00 Uhr und ich merke immer, wie gut mir das tut. Ich fühle mich da viel beweglicher nach der Stunde. Ich weiß gar nicht, wie es den anderen geht, aber ich komme mir immer so verjüngt vor, wenn ich das Wasser verlasse. Das ist wie ein kleiner Jungbrunnen, kann ich dir sagen. Letzte Woche haben wir sogar so eine neue Übung gemacht, bei der man mit den Armen das Wasser wie ein Paddelboot schaufeln muss. Ich sage dir, am nächsten Tag hatte ich richtig Muskelkater – aber es war ein gutes Gefühl!

Donnerstags ist für mich immer der Skat-Tag. Um 14:30 Uhr treffe ich mich mit meiner Skatrunde im Café am Markt. Wir spielen dann, lachen viel und sind richtig in unserem Element. Das ist so ein kleiner Höhepunkt der Woche, weil wir uns immer sehr auf das Spiel freuen. Manchmal geht es auch gar nicht ums Skatspielen, sondern mehr um die Geschichten, die jeder so auf Lager hat. Da kommen dann auch mal die älteren Anekdoten aus der Jugendzeit zum Vorschein. Weißt du, bei uns wird da oft in Erinnerungen geschwelgt. Die Stimmung ist immer gut, und wenn es dann mal wieder eine Runde „alle Neune“ gibt, sind wir fast alle ein bisschen zu laut vor Freude.

Freitag ist dann der Tag, an dem meine Tochter vorbeikommt, um mir beim Aufräumen zu helfen. Sie kommt immer gegen 16:00 Uhr. Ich muss zugeben, ich lasse mich da manchmal ein bisschen gehen und verschiebe es auf den Freitag, aber sie ist echt fleißig. Sie hilft mir nicht nur beim Aufräumen, sondern wir trinken auch zusammen einen Kaffee und quatschen über alles mögliche. Es tut einfach gut, sie um sich zu haben. Da bekommt man auch immer gleich so eine andere Perspektive auf die eigenen Sorgen. Und oft gibt’s dann noch eine Runde von den leckeren Keksen, die ich neulich gebacken habe. Die sind nicht perfekt, aber wer sieht das schon? Sie sind trotzdem immer schnell weg.

Am Wochenende, da gehe ich manchmal zum Seniorennachmittag in meine Kirchengemeinde. Das ist jedes Mal um 14:00 Uhr. Es ist immer eine schöne Mischung aus Gesprächen und kleinen Aktivitäten. Manchmal machen wir Basteln oder Singen, aber immer gibt es auch ein bisschen was zu lachen. Ich hab das Gefühl, die Kirchengemeinde ist eine der wenigen Stellen, wo man wirklich mit Menschen aus der Gegend zusammenkommt. Und das tut auch gut. Neulich habe ich dann sogar eine neue Bekannte getroffen, die früher in meiner Straße gewohnt hat, als wir noch Kinder waren. Das war wie ein kleiner Heimatschlag, als ich ihren Namen gehört habe. Ich glaube, wir gehen demnächst mal zusammen spazieren.

Und dann kommen noch die Ergotherapie-Termine, die zweimal in der Woche stattfinden. Die Termine sind immer flexibel, je nachdem, wie es bei mir passt. Ich freue mich auf jeden Fall immer darauf, weil ich merke, dass mir die Übungen wirklich helfen. Aber manchmal fühlt es sich auch ein bisschen seltsam an, zu üben, was man doch eigentlich schon seit Jahren kann. Doch der Blick von der Therapeutin, der hat was – sie sieht Dinge, die ich selbst nicht bemerke. Aber das ist okay. Es fühlt sich an, als ob ich mit jedem Termin ein bisschen sicherer werde und wieder Dinge zurückgewinne, die ich irgendwann verloren hatte.

Ja, das ist so mein Wochenplan. Es ist ein bisschen viel, aber ich finde, es hält mich auf Trab und bringt mir Freude. Es gibt ja immer so viel zu tun, aber wenn man sich die Zeit nimmt, für die kleinen Dinge, dann hat man auch ein gutes Gefühl."

⚡️ Erstelle einen Wochenplan aus den unsortieren Äußerungen der Klientin.

⚡️ Deine Herausforderung:
1. Gib der KI ein Muster, nach dem es die Informationen zusammenfassen und in Form eines übersichtlichen Wochenplanes bringen soll.
2. Experimentiere mit dem One-Shot Ansatz:
   - Wie detailliert muss das Beispiel sein?
   - Welche Zusatzinformationen sind hilfreich?
   - Wie kannst du Variationen anfordern?

⚡️ Probiere verschiedene Detailgrade in deinen Prompts aus!""",
            "hint": "Tipp: Beobachte, wie unterschiedliche Vorlagen das Ergebnis beeinflussen",
            "example": "Teste verschiedene Detailtiefen: 'Nutze dieses Format...' vs. 'Übernimm diese Struktur, aber mit...' vs. 'Adaptiere diesen Plan für...'"
        }
    },
    "Few-Shot Prompting": {
        "Zielformulierungen": {
            "task": """🎯 Lernziel: Entwickle Few-Shot Prompts zum formulieren von Therapiezielen nach COAST.

⚡️ Ausgangssituation:
Du hast diese Beispiele für Funktionsorientierte Ziele und mögliche daraus resultierende Ziele nach COAST:

'Verbesserung der Handkraft' -> 'Herr B. schreibt (mit seiner rechten Hand) mithilfe eines griffverdickten Stiftes seinen Namen auf ein Formular bis zum Datum.'
'Frau D. ist in der Lage, zum Ende der 10 Einheiten eine Daumenopposition durchzuführen.' -> 'Frau D. schließt ihre Haustür (schmerzfrei) mit dem Schlüssel auf und zu bis zum Datum.'
'regelmäßig und genug Nahrungsaufnahme' -> 'Frau L. nimmt täglich 3 Mahlzeiten selbstständig zu Hause zu sich bis zum Datum.'
'Verbesserung/Erhalt der Gedächtnisfunktion' -> 'Frau M. löst ein einfaches Kreuzworträtsel mit verbaler Anleitung in einer ruhigen Umgebung bis zum Datum.'
'Felix arbeitet konzentriert an seinen Hausaufgaben und lässt sich dabei nicht ablenken.' -> 'Felix erledigt innerhalb einer halben Stunde seine Deutschhausaufgaben mit verbaler Anleitung seiner Mutter bis zum Datum'
'Karl soll eine Aufgabe für 5 Minuten konzentriert bearbeiten, ohne sich dabei ablenken zu lassen.' -> 'Karl erledigt 10 Matheaufgaben selbstständig in 10 Minuten in seiner Schulklasse bis zum Datum.'
'in der Akte: Brot schmieren, im Arztbericht: Erarbeiten von Strategien, um selbstständig das Brot zu schmieren.' -> 'Herr S. bestreicht ein Brot mit weicher Butter selbstständig mit einem griffverdickten Messer bis zum Datum.'
'Erarbeitung von Gedächtnisstrategien' -> 'Herr T. kauft bis zum Datum 5 Zutaten selbstständig im Supermarkt ohne Einkaufzettel ein.'
'hält den Stift im Dreipunktgriff' -> 'Leon hält beim Schreiben einer DIN-A4-Seite den Bleistift im Dreipunktgriff bis zum Datum.'

Quelle: Brinkmann S. COAST – Ziele betätigungsfokussiert … neuroreha 2024; 16: 129–135, Thieme (2024)

Deine Herausforderung:
1. Du möchtest die Zielformulierung üben und dir dafür weitere Ziele nach COAST aus funktionellen oder kurzen Beschreibungen formulieren lassen.
2. Experimentiere mit dem Few-Shot Ansatz:
   - Wie viele Beispiele sind optimal?
   - Wie explizit muss das Muster erklärt werden?
   - Welche Anweisungen helfen der KI den Auftrag zu verstehen?
   - Musst du der KI die COAST-Methode näher erklären?

⚡️ Teste verschiedene Kombinationen von Beispielen!""",
            "hint": "Tipp: Beobachte, wie die Anzahl und Art der Beispiele das Ergebnis beeinflusst",
            "example": "Probiere verschiedene Einleitungen: 'Wandle nach diesen Beispielen um...' vs. 'Folge diesem Muster...' vs. 'Übertrage diese Logik...'"
        },

    },
    "Chain-of-Thought Prompting": {
        "Aushang": {
            "task": """🎯 Lernziel: Entwickle Chain-of-Thought Prompts für die Erstellung eines Aushangs

Ausgangssituation:
Du möchtest in der WfbM einen Aushang in leichter Sprache machen, in dem das neue Angebot "Morgensportrunde" angekündigt wird.
Der Morgensport findet jeden Tag um 9 Uhr statt und eingeladen sind alle Mitarbeiter*innen der Werkstatt, die Lust haben, aktiv in den Tag zu starten.

Deine Herausforderung:
1. Identifiziere die notwendigen Denkschritte:
   - Inhaltliche Gestaltung des Aushangs
   - Zielgruppenanalyse
   - Informationsaufbereitung
   - Formatentscheidung
   - ...(welche Schritte erscheinen dir noch als sinnvoll?)
2. Experimentiere mit verschiedenen Prompt-Strukturen:
   - Wie detailliert müssen die Zwischenschritte sein?
   - Welche Verbindungen zwischen den Schritten sind wichtig?
   - Wie führst du zur Lösung?

⚡️ Teste verschiedene Arten, die Denkschritte zu formulieren!""",
            "hint": "Tipp: Überleg einmal: Wie würdest du an die Aufgabe heran gehen, wenn du sie ohne KI erledigen würdest? Zerlege deine Herangehensweise in Teilschritte und gib diese der KI mit auf den Weg.",
            "example": "Probiere verschiedene Verknüpfungen: 'Gehe diese Schritte durch...' vs. 'Entwickle aufbauend auf...' vs. 'Leite Schritt für Schritt her...'"
        }
    },
    "Skala Prompting": {
        "Was ist Betätigung?": {
            "task": """🎯 Lernziel: Entwickle Skala-Prompts für verschiedene Sprachniveaus

⚡️ Ausgangssituation:
Häufig kommen Klient*innen mit Anliegen zu dir, die eher funktionell sind ("Ich möchte, dass meine Hand wieder funktioniert."). Es bereitet immer wieder Schwierigkeiten, deutlich zu machen, was eine Betätigung eigentlich ist. Du hast dir deshalb überlegt, dir die Definition vom DVE mal in unterschiedlichen Sprachniveaus aufbereiten zu lassen.
Du hast folgende Definition von Betätigung:

"Unter Betätigung verstehen Ergotherapeuten die Summe von Aktivitäten und Aufgaben des täglichen Lebens, die durch Individuen und Kultur benannt, strukturiert und mit Bedeutung versehen sind. Betätigungen werden individuell unterschiedlich ausgeführt, sind Ausdruck unserer Persönlichkeit und lassen uns fortlaufend mit unserer Umwelt interagieren. Betätigung gehört zu den Grundbedürfnissen des Menschen und umfasst alles, was Menschen tun. Dazu gehören Tätigkeiten zur Versorgung der eigenen Person (Selbstversorgung), zum Genuss des Lebens (Freizeit) und als Beitrag zur sozialen und ökonomischen Entwicklung des Individuums und der Gemeinschaft (Produktivität). Bedeutungsvolle Aktivitäten sind für den Menschen dadurch charakterisiert, dass sie zielgerichtet sind und als signifikant, sinnvoll und wertvoll für den Einzelnen empfunden werden“. 
(Quelle: Kohlhuber, Ergotherapie - betätigunszentriert in Ausbildung und Praxis, 2020 Georg Thieme Verlag (2020) - Nach DVE)

⚡️ Deine Herausforderung:
1. Definiere die Skalenendpunkte:
   - Was charakterisiert Stufe 1 (Alltagssprache)?
   - Was charakterisiert Stufe 10 (Expertensprache)?
2. Frage die KI zunächst, wo auf der Skala sie die Definition einsortieren würde.
3. Verschiebe den Text auf der Skala.
2. Experimentiere mit verschiedenen Prompt-Varianten:
   - Versuche mal, andere Endpunkte zu wählen z.B. 1=Übelster TikTok-Slang, 10=Elaborierte Fachsprache
   - Definierst du die Zwischenstufen?
   - Welche Aspekte der Sprache sollen sich ändern?
   - Wie konkret müssen die Anweisungen sein?

⚡️ Teste verschiedene Skalendefinitionen und ihre Wirkung!""",
            "hint": "Tipp: Beobachte, wie unterschiedliche Skalenbeschreibungen das Ergebnis beeinflussen",
            "example": "Probiere verschiedene Formulierungen: 'Auf einer Skala von...' vs. 'Passe den Fachjargon an...' vs. 'Variiere die Komplexität...'"
        },
        "Was ist Ergotherapie?": {
            "task": """🎯 Lernziel: Entwickle Skala-Prompts für Übungsanleitungen

⚡️ Ausgangssituation:
Du möchtest für einen Flyer gern erklären, was Ergotherapie ist. Dafür hast du dir die Definition vom DVE kopiert:

"Ergotherapie unterstützt und begleitet Menschen jeden Alters, die in ihrer Handlungsfähigkeit eingeschränkt oder von Einschränkung bedroht sind. Ziel ist, sie bei der Durchführung für sie bedeutungsvoller Betätigungen in den Bereichen Selbstversorgung, Produktivität und Freizeit in ihrer persönlichen Umwelt zu stärken.
Hierbei dienen spezifische Aktivitäten, Umweltanpassung und Beratung dazu, dem Menschen Handlungsfähigkeit im Alltag, gesellschaftliche Teilhabe und eine Verbesserung seiner Lebensqualität zu ermöglichen."
(Quelle: https://dve.info/ergotherapie/definition (Stand: 15.11.24))

⚡️ Deine Herausforderung:
1. Definiere die Skalenendpunkte:
   - Was charakterisiert Stufe 1 (Alltagssprache)?
   - Was charakterisiert Stufe 10 (Expertensprache)?
2. Frage die KI zunächst, wo auf der Skala sie die Definition einsortieren würde.
3. Verschiebe den Text auf der Skala.
2. Experimentiere mit verschiedenen Prompt-Varianten:
   - Versuche mal, andere Endpunkte zu wählen z.B. 1=Übelster TikTok-Slang, 10=Elaborierte Fachsprache
   - Definierst du die Zwischenstufen?
   - Welche Aspekte der Sprache sollen sich ändern?
   - Wie konkret müssen die Anweisungen sein?

⚡️ Probiere verschiedene Komplexitätsabstufungen aus!""",
            "hint": "Tipp: Achte darauf, wie verschiedene Komplexitätsdefinitionen das Ergebnis beeinflussen",
            "example": "Teste verschiedene Ansätze: 'Vereinfache auf Stufe...' vs. 'Erhöhe die Komplexität auf...' vs. 'Passe die Detailtiefe an...'"
        }
    }
}

technique_intros = {
    "Zero-Shot Prompting": {
        "title": "Zero-Shot Prompting 🎯",
        "description": """Zero-Shot Prompting ist wie eine präzise Anweisung - du sagst genau, was du willst, ohne Beispiele zu geben.

Kernelemente eines guten Zero-Shot Prompts:
• Klare, spezifische Anweisungen
• Definierte Rahmenbedingungen
• Gewünschtes Format oder Struktur
• Zielgruppe und Kontext

Diese Technik eignet sich besonders für:
• Standardisierte Dokumente
• Klare Arbeitsanweisungen
• Strukturierte Informationen
• Eindeutige Anfragen

🤔 Denk dran: Je präziser deine Anweisung, desto besser das Ergebnis!"""
    },
    "One-Shot Prompting": {
        "title": "One-Shot Prompting 📝",
        "description": """One-Shot Prompting nutzt ein einzelnes Beispiel als Vorlage - wie eine Schablone für das gewünschte Ergebnis.

So funktioniert's:
1. Ein Beispiel vorgeben
2. Klare Parallelen aufzeigen
3. Neue Parameter definieren
4. Gewünschte Anpassungen beschreiben

Besonders nützlich für:
• Dokumentenvorlagen
• Standardisierte Berichte
• Einheitliche Formulierungen
• Formatanpassungen

💡 Tipp: Das Beispiel sollte möglichst genau deinem Wunschergebnis entsprechen!"""
    },
    "Few-Shot Prompting": {
        "title": "Few-Shot Prompting 🎯🎯🎯",
        "description": """Few-Shot Prompting verwendet mehrere Beispiele, um ein Muster zu etablieren - wie das Lernen aus verschiedenen Vorlagen.

Wichtige Aspekte:
• 2-3 aussagekräftige Beispiele
• Erkennbares Muster
• Klare Transformation
• Konsistente Struktur

Ideal geeignet für:
• Komplexe Umformulierungen
• Stilanpassungen
• Musterbasierte Aufgaben
• Verschiedene Variationen

✨ Tipp: Die Beispiele sollten verschiedene Aspekte des gewünschten Ergebnisses abdecken!"""
    },
    "Chain-of-Thought Prompting": {
        "title": "Chain-of-Thought Prompting 🔄",
        "description": """Chain-of-Thought Prompting strukturiert komplexe Aufgaben in einzelne Denkschritte - wie eine Schritt-für-Schritt-Anleitung.

Zentrale Elemente:
• Logische Abfolge
• Verbundene Denkschritte
• Klare Zwischenergebnisse
• Nachvollziehbare Entwicklung

Perfekt für:
• Komplexe Entscheidungen
• Mehrstufige Prozesse
• Strukturierte Analysen
• Logische Ableitungen

🎯 Tipp: Je klarer die einzelnen Denkschritte, desto besser das Endergebnis!"""
    },
    "Skala Prompting": {
        "title": "Skala Prompting 📊",
        "description": """Skala Prompting ermöglicht die gezielte Anpassung von Inhalten entlang einer definierten Skala - wie ein Regler für verschiedene Ebenen.

Wichtige Komponenten:
• Klare Skalenendpunkte
• Definierte Abstufungen
• Konkrete Merkmale je Stufe
• Gewünschte Anpassungsrichtung

Besonders effektiv für:
• Sprachniveauanpassungen
• Komplexitätssteuerung
• Zielgruppengerechte Kommunikation
• Flexible Formatierung

⚖️ Tipp: Eine klare Definition der Skalenendpunkte ist entscheidend!"""
    }
}

def display_hints_and_examples(technique, exercise):
    with st.expander("💡 Hilfen & Beispiele", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💭 Tipps")
            st.markdown(task_messages[technique][exercise]["hint"])
            
        with col2:
            st.markdown("### ✨ Beispiele")
            st.markdown(task_messages[technique][exercise]["example"])

def get_teacher_feedback(technique, exercise=None):
    """Generiert kontextspezifisches Feedback vom Teacher"""
    current_task = task_messages[technique]
    if isinstance(current_task, dict):
        current_task = current_task[exercise]["task"] if exercise else current_task["task"]
    
    teacher_prompt = f"""Als erfahrener Prompting-Lehrer analysiere den bisherigen Übungsverlauf:
    
    Aktuelle Technik: {technique}
    Aktuelle Aufgabe: {current_task}
    
    Gesprächsverlauf:
    {str(st.session_state.displayed_messages)}
    
    Gib folgendes Feedback:
    1. Erkläre kurz die aktuelle Prompting-Technik, falls du schächen erkennst.
    2. Analysiere die bisherigen Prompting-Versuche und gibt konkrete Verbesserungsvorschläge.
    3. Motiviere zum erneuten Üben, wenn du die notwendigkeit siehst. Ansonsten rate dazu, dass der User sich die nächste Technik anschaut.
    
    Bleibe dabei immer unterstützend und konstruktiv."""
    
    teacher_messages = [
        {"role": "system", "content": st.session_state.teacher_sys_prompt},
        {"role": "user", "content": teacher_prompt}
    ]
    
    try:
        response = client.chat.completions.create(
            model=st.session_state.teacher_model,
            messages=teacher_messages,
            temperature=st.session_state.teacher_temp
        )
        
        feedback = response.choices[0].message.content
        st.session_state.teacher_messages.append({
            "role": "assistant", 
            "content": feedback
        })
        
        return feedback
    except:
        try:
            response = client.chat.completions.create(
            model=st.session_state.teacher_model_if_error,
            messages=teacher_messages,
            temperature=st.session_state.teacher_temp
        )
        
            feedback = response.choices[0].message.content
            st.session_state.teacher_messages.append({
                "role": "assistant", 
                "content": feedback
            })

        except Exception as e:
            return f"Ups, da ist etwas schiefgegangen: {str(e)}"

# Seitenleiste
with st.sidebar:
    st.header("Prompting-Techniken")
            
    technique = st.selectbox(
        "Wähle eine Technik:",
        ["Zero-Shot Prompting",
         "One-Shot Prompting",
         "Few-Shot Prompting",
         "Chain-of-Thought Prompting",
         "Skala Prompting"]
    )

    if technique == "Zero-Shot Prompting":
        exercise = st.selectbox(
            "Wähle eine Übung:",
            ["Informationsblatt Ergonomie",
             "Traumreise"]
        )
    elif technique == "One-Shot Prompting":
        exercise = st.selectbox(
            "Wähle eine Übung:",
            ["Dokumentation",
             "Wochenplan"]
        )
    elif technique == "Few-Shot Prompting":
        exercise = st.selectbox(
            "Wähle eine Übung:",
            ["Zielformulierungen"]
        )
    elif technique == "Chain-of-Thought Prompting":
        exercise = st.selectbox(
            "Wähle eine Übung:",
            ["Aushang"]
        )
    elif technique == "Skala Prompting":
        exercise = st.selectbox(
            "Wähle eine Übung:",
            ["Was ist Betätigung?",
             "Was ist Ergotherapie?"]
        )
    
    if st.button("Technik üben"):
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.sop_sys_prompt}]
        
        # Speichere aktuelle Technik und Übung
        st.session_state.current_technique = technique
        st.session_state.current_exercise = exercise

        task = task_messages[technique][exercise]["task"]

        st.session_state.displayed_messages = []

        st.success(f"Alles klar, lass uns {technique} üben!")

    if st.button("Neues Gespräch starten"):
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.sop_sys_prompt}]
        
        # Speichere aktuelle Technik und Übung
        st.session_state.current_technique = technique
        st.session_state.current_exercise = exercise

        task = task_messages[technique][exercise]["task"]
    
        st.session_state.displayed_messages = []
        st.success(f"Alles klar, auf ein Neues...lass uns {technique} üben!")


# Teacher Bereich
    st.markdown("---")
        
    @st.dialog("🎓 Prompting Teacher")
    def teacher():
        if st.button("Frag den Teacher um Rat", help="Lass dir Tipps zur aktuellen Übung geben"):
            with st.spinner("Der Teacher schat sich deine Übung an..."):
                feedback = get_teacher_feedback(
                    technique, 
                    exercise
                )
                with st.chat_message("teacher", avatar="🎓"):
                    st.markdown(feedback)


        # Teacher Verlauf
        with st.expander("📚 Teacher Verlauf", False):
            if st.session_state.teacher_messages:
                for idx, msg in enumerate(st.session_state.teacher_messages):
                    st.markdown(f"**Feedback {idx+1}:**")
                    st.markdown(msg["content"])
                    st.markdown("---")
            else:
                st.info("Noch kein Feedback vom Teacher vorhanden. Klick auf 'Frag den Teacher um Rat' um Unterstützung zu bekommen!")

    if st.button("🎓 Prompting Teacher"):
        teacher()

def display_chat():
    for message in st.session_state.displayed_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_input():
    if prompt := st.chat_input("Schreib mir..."):
        st.session_state.displayed_messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model=st.session_state.sop_model,
                    messages=st.session_state.messages,
                    temperature=st.session_state.sop_temp,
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
            except:
                try:
                    response = client.chat.completions.create(
                        model=st.session_state.sop_model_if_error,
                        messages=st.session_state.messages,
                        temperature=st.session_state.sop_temp,
                    )
                    full_response = response.choices[0].message.content
                    st.markdown(full_response)
                except Exception as e:
                    return f"Ups, da ist etwas schiefgegangen: {str(e)}"

        st.session_state.displayed_messages.append({"role": "assistant", "content": full_response})
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if "current_technique" in st.session_state and "current_exercise" in st.session_state:
    technique = st.session_state.current_technique
    exercise = st.session_state.current_exercise
    
    # Technik-Intro anzeigen
    st.markdown(f"## {technique_intros[technique]['title']}")
    with st.expander("ℹ️ Über diese Technik", expanded=False):
        st.markdown(technique_intros[technique]['description'])
    
    # Aufgabe anzeigen
    st.markdown("### 🎯 Deine Aufgabe")
    st.markdown(task_messages[technique][exercise]["task"])
    
    # Hints und Examples anzeigen
    display_hints_and_examples(technique, exercise)

# Chat anzeigen
display_chat()
process_input()
