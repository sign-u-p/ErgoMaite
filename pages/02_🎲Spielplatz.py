import streamlit as st
import openai

import db
import pw_check as pw
import parameters as par

#Passwort checken
if pw.check_password() == False:
    st.stop()  # Do not continue if check_password is not True.


# Initialisiere session_state-variablen
if "bot" not in st.session_state:
    st.session_state["bot"] = db.get_bot_spielplatz("Spielplatzpirat")
# Session-Variables initialisieren
if "bot_name" not in st.session_state:
        st.session_state["bot_name"] = st.session_state.bot["bot_name"]
if "sys_prompt" not in st.session_state:
        st.session_state["sys_prompt"] = st.session_state.bot["sys_prompt"]
if "model" not in st.session_state:
        st.session_state["model"] = st.session_state.bot["model"]
if "temp" not in st.session_state:
    st.session_state["temp"] = st.session_state.bot["temp"]
#if "prefix" not in st.session_state:
#        st.session_state["prefix"] = st.session_state.bot["prefix"]
#if "injection" not in st.session_state:
#        st.session_state["injection"] = st.session_state.bot["injection"]
#if "messages" not in st.session_state:
#        if st.session_state.prefix != None:
#            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt},
#                                        {"role": "assistant", "content": st.session_state.prefix}]
#        else:
st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
st.session_state["Komme_vom_Spielplatz"] = True

if st.session_state.bot_name == "initial_spielplatz":
    st.markdown(f"> 🎲")
else:
    st.markdown(f"> **{st.session_state.bot_name}** @ 🎲")

#ToDo: Beschreibung anpassen
with st.expander("Wie geht das hier?"):
    st.markdown("In der Navigationsleiste auf der linken Seite siehst du ein Eingabefeld (Sollte die Navigationsleiste nicht ausgeklappt sein, klicke auf den winzigen Pfeil in der linken oberen Ecke).\n"
                "In dieses Feld kannst du eine Rolle eingeben, die dein Bot annehmen soll. An dieser orientiert sich der Bot in jeder folgenden Konversation.")
    st.markdown("Wenn du mit weiteren Einstellungen herumspielen möchtest, kannst du das unter dem Reiter \"Forgeschritten\" unterhalb des Eingabefeldes tun.")
    st.markdown("Hast du eine Idee für eine Rolle, die du im Unterricht nutzen könntest? Teile sie doch mir einem Klick auf \"Propmt im Sandkasten teilen\".")
    st.markdown("**Viel Spaß! :)**")

st.title("Let`s learn.")

openai.api_key=st.secrets["OPENAI_API_KEY"]

# Seitenleiste
with st.sidebar:
    st.header("Werkzeuge")

    with st.form(key='create_bot'):
        wst_bot_name = st.text_input(value=st.session_state.bot_name,placeholder="Wie heist dein Bot?", label="Botname")
    # ToDo: Hinweis platzieren, dass der Name keinen Einfluss auf das Verhalten des Bots hat.

        wst_sys_prompt = st.text_area(value=st.session_state.sys_prompt,placeholder="Gib deinem Bot eine Rolle.", label="Systemprompt")


        wst_temp = st.slider("Temperature", 0.0, 1.0, st.session_state.temp)
        if "temp" in st.session_state:
            st.markdown(f"**Momentan gewählte Temperature: {st.session_state.temp}**")
        with st.expander("Was bedeutet Temperature?"):
            st.markdown("**Die Temperature ist das \"Gemüt\" deines Bots.** Soll er/sie eher (0) direkt, wenig experimentierfreudig und tendenziell verlässlicher oder (1) fantasievoll, überraschend und eher weniger an Fakten gebunden sein?")
            st.markdown("An dieser Stelle einmal der Hinweis: Halluzinationen sind noch immer ein Problem großer Sprachmodelle - Unabhängig von deren Einstellungen. Die Informationen, die die Bots liefern sind nicht verlässlich und sollten niemals Grundlage von wichtigen Entscheidungen sein. **Die Antworten klingen in der Regel super eloquent. Das ist aber kein Maßstab für deren Richtigkeit!**")

#ToDo: Modellliste in die db
        wst_model = st.selectbox(
            "Modell",
            ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0
        )
        if "model" in st.session_state:
            st.markdown(f"**Momentan aktives Modell: {st.session_state.model}**")
        with st.expander("Was bedeutet Modell?"):
            st.markdown("**Das Sprachmodell ist das Herzstück des Bots.** Hier fließen die Informationen zusammen und die Antworten werden generiert.\n"
                        "Wir nutzen die Sprachmodelle von *Open AI*. Es gibt aber eine ganze Reihe weiterer Sprachmodelle mit guten Leistungen.\n"
                        "Voreingestellt ist das Modell mit der aktuell besten Leistung. Falls du nichts spezielles damit vor hast, lass das ruhig einfach so. Es kann aber ganz interessant sein, mal zu schauen, welche unterschiedlichen Antworten die Modelle bringen.")


        if st.form_submit_button("Einstellungen probieren"):
            st.session_state["bot_name"] = wst_bot_name
            st.session_state["model"] = wst_model
            st.session_state["sys_prompt"] = wst_sys_prompt
            st.session_state["temp"] = wst_temp
            st.session_state.messages=[{"role":"system", "content":st.session_state.sys_prompt}]
            st.success("Kann los gehen: Einstellungen übernommen.")
            st.write(st.session_state.bot_name)
            st.write(st.session_state.sys_prompt)

    if st.button("Neues Gespräch starten"):
        st.session_state.messages=[{"role":"system", "content":st.session_state.sys_prompt}]
        st.success("Alright..dann auf ein Neues ;)")


# Im Sandkasten teilen
    #if st.button('**Bot im Sandkasten teilen**'):
        # Liste erstellen mit Prompt, Temp und Model
        #bot = ({"bot_name":st.session_state.bot_name,
        #"sys_prompt":st.session_state.sys_prompt,
        #"temp":st.session_state.temp,
        #"model":st.session_state.model})
        # ToDo: Test einfügen, ob der Name/Prompt bereits existiert.
        # Liste an db übergeben
        #if db.insert_bot_sandkasten(bot) == False:
        #    st.error("Es gibt schon einen Bot mit diesem Namen.")
        #else:
        #    st.success('Prompt im Sandkasten geteilt.')

# Chatnachrichten darstellen
def display_input():
    for message in st.session_state.messages:
        if message["role"]=="system":
            pass
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Userinput und response bearbeiten
def process_input():
    if prompt := st.chat_input("Lass' mal reden."):
        if st.session_state.messages == []:
            st.session_state.messages.append({"role":"system", "content":st.session_state.sys_prompt})
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["model"],
                temperature=st.session_state["temp"],
                messages=st.session_state.messages,
     #               {"role":"system", "content": "Du bist ein Auto"},
     #               {"role": m["role"], "content": m["content"]}
     #               for m in st.session_state.messages],
                stream=True
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response+"|")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

display_input()
process_input()
