import streamlit as st

import openai

import db
import parameters as par

#import pw_check as pw

# Passwort checken
#if pw.check_password() == False:
#    st.stop()  # Do not continue if check_password is not True.

openai.api_key=st.secrets["OPENAI_API_KEY"]

# state variablen initialisieren
if "Komme_vom_Spielplatz" not in st.session_state:
    st.session_state["Komme_vom_Spielplatz"] = False
if st.session_state["Komme_vom_Spielplatz"] == True:
        #Bot aus der mongodb holen
        st.session_state["bot"] = db.get_bot(par.initial)
        #Session-Variables initialisieren
        st.session_state["bot_name"] = st.session_state.bot["bot_name"]
        st.session_state["sys_prompt"] = st.session_state.bot["sys_prompt"]
        st.session_state["model"] = st.session_state.bot["model"]
        st.session_state["temp"] = st.session_state.bot["temp"]
        st.session_state["prefix"] = st.session_state.bot["prefix"]
        st.session_state["injection"] = st.session_state.bot["injection"]
        st.session_state["explanation_title"] = st.session_state.bot["explanation_title"]
        st.session_state["explanation_text"] = st.session_state.bot["explanation_text"]
        st.session_state["explanation_text_second"] = st.session_state.bot["explanation_text_second"]
        if st.session_state.prefix != None:
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt},
                                        {"role": "assistant", "content": st.session_state.prefix}]
        else:
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
# Bot aus der mongodb holen
if "bot_name" not in st.session_state:
    st.session_state["bot"] = db.get_bot(par.initial)

    # Session-Variables initialisieren
    if "bot_name" not in st.session_state:
            st.session_state["bot_name"] = st.session_state.bot["bot_name"]
    if "sys_prompt" not in st.session_state:
            st.session_state["sys_prompt"] = st.session_state.bot["sys_prompt"]
    if "model" not in st.session_state:
            st.session_state["model"] = st.session_state.bot["model"]
    if "temp" not in st.session_state:
        st.session_state["temp"] = st.session_state.bot["temp"]
    if "prefix" not in st.session_state:
        st.session_state["prefix"] = st.session_state.bot["prefix"]
    if "injection" not in st.session_state:
        st.session_state["injection"] = st.session_state.bot["injection"]
    if "explanation_title" not in st.session_state:
        st.session_state["explanation_title"] = st.session_state.bot["explanation_title"]
    if "explanation_text" not in st.session_state:
        st.session_state["explanation_text"] = st.session_state.bot["explanation_text"]
    if "explanation_text_second" not in st.session_state:
        st.session_state["explanation_text_second"] = st.session_state.bot["explanation_text_second"]
    if "messages" not in st.session_state:
            if st.session_state.prefix != None:
                st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt},
                                            {"role": "assistant", "content": st.session_state.prefix}]
            else:
                st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
    st.session_state["Komme_vom_Spielplatz"] = False


# state-variablen der Wahl des Bots entsprechend anpassen
def update_selection(selected):
    st.session_state.bot = db.get_bot(selected)
    st.session_state["bot_name"] = st.session_state.bot["bot_name"]
    st.session_state["sys_prompt"] = st.session_state.bot["sys_prompt"]
    st.session_state["model"] = st.session_state.bot["model"]
    st.session_state["temp"] = st.session_state.bot["temp"]
    st.session_state["prefix"] = st.session_state.bot["prefix"]
    st.session_state["injection"] = st.session_state.bot["injection"]
    st.session_state["explanation_title"] = st.session_state.bot["explanation_title"]
    st.session_state["explanation_text"] = st.session_state.bot["explanation_text"]
    st.session_state["explanation_text_second"] = st.session_state.bot["explanation_text_second"]

# ToDo: Injektionen funktionieren noch nicht

    if st.session_state.prefix != None:
        st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt},
                                    {"role": "assistant", "content": st.session_state.prefix}]
    else:
        st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]

    if st.session_state.injection != None:
        st.session_state.injection = st.session_state.injection.append(
            {"role": "user", "content": st.session_state.injection})
    else:
        pass


with st.sidebar:
    st.session_state["choice"] = db.get_choice()
    #st.session_state["choice"] =["Conrad", "Prosa"]
    st.session_state["selected"]=st.selectbox("Mit wem magst du reden?",st.session_state["choice"])
    if st.button("Bot wählen"):
        update_selection(st.session_state.selected)
        st.success(f"Du bist jetzt mit **{st.session_state.bot_name}** verbunden.")
    if st.button("Neues Gespräch starten"):
        st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
        st.success(f"Alles klaro...ein neues Gespräch mit **{st.session_state.bot_name}** ist gestartet.")


st.markdown(f"> {st.session_state.bot_name} @ 🎠")
if st.session_state.explanation_title != None:
    with st.expander(st.session_state.explanation_title, False):
        st.markdown(st.session_state.explanation_text)
        if st.session_state.explanation_text_second != None:
            st.markdown(st.session_state.explanation_text_second)


def display_input():
    for message in st.session_state.messages:
        if message["role"]=="system":
            pass
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def process_input():
    if prompt := st.chat_input("Lass' mal reden."):
    #    if st.session_state.messages == []:
    #        st.session_state.messages.append({"role":"system", "content":st.session_state.sys_prompt})
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["model"],
                temperature=st.session_state["temp"],
                messages=st.session_state["messages"],
    #                {"role":"system", "content": "Du bist ein Auto"},
    #                {"role": m["role"], "content": m["content"]}
    #                for m in st.session_state.messages],
                stream=True
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response+"|")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

display_input()
process_input()

#ToDo: Konversation geht nicht weiter...update openai-chathistory
#ToDo: