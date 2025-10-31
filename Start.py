import streamlit as st

import db

import pw_check as pw

# Passwort checken
if pw.check_password() == False:
    st.stop()

if "start" not in st.session_state:
    st.session_state["start"] = db.get_start()
if "start_title" not in st.session_state:
    st.session_state["start_title"] = st.session_state.start["title"]
if "start_text_1" not in st.session_state:
    st.session_state["start_text_1"] = st.session_state.start["text_1"]
if "start_text_2" not in st.session_state:
    st.session_state["start_text_2"] = st.session_state.start["text_2"]
if "start_text_3" not in st.session_state:
    st.session_state["start_text_3"] = st.session_state.start["text_3"]
if "start_text_4" not in st.session_state:
    st.session_state["start_text_4"] = st.session_state.start["text_4"]
if "start_text_5" not in st.session_state:
    st.session_state["start_text_5"] = st.session_state.start["text_5"]
if "start_text_6" not in st.session_state:
    st.session_state["start_text_6"] = st.session_state.start["text_6"]

st.markdown("> Start")
if st.session_state.start_title != None:
    st.title(st.session_state.start_title)
    if st.session_state.start_title == 1:
        with st.expander("...mehr..."):
            st.markdown("Test")
if st.session_state.start_text_1 != None:
    st.markdown(st.session_state.start_text_1)
if st.session_state.start_text_2 != None:
    st.markdown(st.session_state.start_text_2)
if st.session_state.start_text_3 != None:
    st.markdown(st.session_state.start_text_3)
if st.session_state.start_text_4 != None:
    st.markdown(st.session_state.start_text_4)
if st.session_state.start_text_5 != None:
    st.markdown(st.session_state.start_text_5)
if st.session_state.start_text_6 != None:
    st.markdown(st.session_state.start_text_6)