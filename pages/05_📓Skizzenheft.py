import streamlit as st
import db

import pw_check as pw

#Passwort checken
if pw.check_password() == False:
    st.stop()  # Do not continue if check_password is not True.

st.markdown(f"> 📓")

if "image_list" not in st.session_state:
    st.session_state["image_list"] = []


st.session_state["pic_count"] = 0

col1, col2, col3 = st.columns(3)

for picture in st.session_state.image_list:
    st.session_state.pic_count += 1
    #pic_count_name = f"share_pic{st.session_state.pic_count}"
    if st.session_state.pic_count % 3 == 0:
        with col3:
            with st.form(f"{st.session_state.pic_count}"):
              st.image(picture[0])
              st.markdown(f"***{picture[1]}***")
              if st.form_submit_button("In der Galerie teilen"):
                st.session_state.image = ({"image_url": picture[0],
                                           "prompt": picture[1]})
                if db.add_image(st.session_state.image) == False:
                  st.error("Das Bild ist schon in der Galerie.")
                else:
                  st.success('Alles klaro...Dein Bild kann jetzt in der Galerie bewundert werden.')
    elif st.session_state.pic_count % 2 == 0:
        with col2:
            with st.form(f"{st.session_state.pic_count}"):
              st.image(picture[0])
              st.markdown(f"***{picture[1]}***")
              if st.form_submit_button("In der Galerie teilen"):
                st.session_state.image = ({"image_url": picture[0],
                                           "prompt": picture[1]})
                if db.add_image(st.session_state.image) == False:
                  st.error("Das Bild ist schon in der Galerie.")
                else:
                  st.success('Alles klaro...Dein Bild kann jetzt in der Galerie bewundert werden.')
    else:
        with col1:
            with st.form(f"{st.session_state.pic_count}"):
              st.image(picture[0])
              st.markdown(f"***{picture[1]}***")
              if st.form_submit_button("In der Galerie teilen"):
                st.session_state.image = ({"image_url": picture[0],
                                           "prompt": picture[1]})
                if db.add_image(st.session_state.image) == False:
                  st.error("Das Bild ist schon in der Galerie.")
                else:
                  st.success('Alles klaro...Dein Bild kann jetzt in der Galerie bewundert werden.')
