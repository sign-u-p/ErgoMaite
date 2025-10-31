import streamlit as st
import time
import openai
from openai import OpenAI

import db
import parameters as par
import llm_provider
import chat_ui

import pw_check as pw

# Passwort checken
if pw.check_password() == False:
    st.stop()

# Inject modern chat UI CSS
chat_ui.inject_chat_css()

openai.api_key=st.secrets["OPENAI_API_KEY"]
client = OpenAI()

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
        st.session_state["model_if_error"] = st.session_state.bot["model_if_error"]
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
    if "model_if_error" not in st.session_state:
        st.session_state["model_if_error"] = st.session_state.bot["model_if_error"]
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
    st.session_state["model_if_error"] = st.session_state.bot["model_if_error"]
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
    st.header("🎠 Bot-Auswahl")
    st.session_state["choice"] = db.get_choice()
    st.session_state["selected"]=st.selectbox("Mit wem magst du reden?",st.session_state["choice"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓ Bot wählen", use_container_width=True):
            update_selection(st.session_state.selected)
            chat_ui.show_success_message(f"Du bist jetzt mit **{st.session_state.bot_name}** verbunden.")

    with col2:
        if st.button("🔄 Neues Gespräch", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
            chat_ui.show_success_message(f"Neues Gespräch mit **{st.session_state.bot_name}** gestartet.")

    st.markdown("---")
    st.markdown(f"**Aktueller Bot:** {st.session_state.bot_name}")
    st.markdown(f"**Modell:** `{st.session_state.model}`")

# Display modern chat header
chat_ui.display_chat_header(
    bot_name=st.session_state.bot_name,
    model=st.session_state.model,
    description="🎠 KI-Russell - Deine KI-gestützten Lernbegleiter"
)

if st.session_state.explanation_title != None:
    with st.expander(f"ℹ️ {st.session_state.explanation_title}", False):
        st.markdown(st.session_state.explanation_text)
        if st.session_state.explanation_text_second != None:
            st.markdown(st.session_state.explanation_text_second)


def display_input():
    """Display chat messages with modern styling"""
    chat_ui.display_modern_chat_messages(st.session_state.messages, show_system=False)


def process_input():
    """Process user input with modern UI feedback"""
    if prompt := chat_ui.create_chat_input_with_placeholder("Lass' mal reden..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=chat_ui.get_avatar("user")):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=chat_ui.get_avatar("assistant")):
            with st.spinner(f"💭 {st.session_state.bot_name} denkt nach..."):
                full_response = ""
                try:
                    full_response = llm_provider.call_llm(
                        model=st.session_state["model"],
                        temperature=st.session_state["temp"],
                        messages=st.session_state["messages"]
                    )
                    st.markdown(full_response)
                except Exception as e:
                    # First retry after 5 seconds
                    try:
                        time.sleep(5)
                        full_response = llm_provider.call_llm(
                            model=st.session_state["model"],
                            temperature=st.session_state["temp"],
                            messages=st.session_state["messages"]
                        )
                        st.markdown(full_response)
                    except:
                        # Fallback to model_if_error
                        try:
                            st.info(f"⚠️ Wechsle zu Fallback-Modell: {st.session_state['model_if_error']}")
                            full_response = llm_provider.call_llm(
                                model=st.session_state["model_if_error"],
                                temperature=st.session_state["temp"],
                                messages=st.session_state["messages"]
                            )
                            st.markdown(full_response)
                        except Exception as final_error:
                            error_msg = f"Fehler bei der Verarbeitung: {str(final_error)}"
                            chat_ui.show_error_message(error_msg)
                            full_response = "Entschuldigung, es gab einen Fehler bei der Verarbeitung deiner Anfrage."

        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})

display_input()
process_input()

#ToDo: Konversation geht nicht weiter...update openai-chathistory
#ToDo:
