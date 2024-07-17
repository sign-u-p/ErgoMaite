import streamlit as st

import db
import pw_check as pw

#Passwort checken
if pw.check_password() == False:
    st.stop()  # Do not continue if check_password is not True.

st.markdown(f"> 🖼️")

col1, col2, col3 = st.columns(3)

st.session_state["column_count_galerie"] = 0
st.session_state["image_list_galerie"] = db.get_all_images()

for image_url in st.session_state.image_list_galerie:
    st.session_state.column_count_galerie += 1
    image = db.search_image(image_url)
    prompt = image["prompt"]
    if st.session_state.column_count_galerie % 3 == 0:
        with col3:
            st.image(image_url)
            st.markdown(prompt)
    elif st.session_state.column_count_galerie % 2 == 0:
        with col2:
            st.image(image_url)
            st.markdown(prompt)
    else:
        with col1:
            st.image(image_url)
            st.markdown(prompt)