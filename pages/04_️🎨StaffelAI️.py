import streamlit as st
import openai
from openai import OpenAI
import db
import pw_check as pw
import parameters as par

#Passwort checken
if pw.check_password() == False:
    st.stop()  # Do not continue if check_password is not True.

client = OpenAI()
if "image_url" not in st.session_state:
  st.session_state["image_url"] = ""
if "image_list" not in st.session_state:
  st.session_state["image_list"] = []
if "image" not in st.session_state:
  st.session_state["image"] = ()

st.markdown(f"> 🎨")
with st.expander("Wie geht das hier?"):
  st.markdown("Hier ist der Ort, an dem du aus Text Bilder machen kannst. Gibt unten deinen Prompt ein, Klicke auf \"Zeig\' her\" und lasse dich überraschen.")
  st.markdown("Alle deine Kreationen aus dieser Sitzung erscheinen im 📓 Skizzenheft. Dort gelangst du über die Seitenleiste hin.")
  st.markdown("Um Bilder mit dem ganzen Kurs zu teilen, klicke **im Skizzenheft** auf den \"Teilen\"-Button unter dem jeweiligen Bild.")
st.title("Let`s draw.")

openai.api_key=st.secrets["OPENAI_API_KEY"]

def create_image(prompt):
  response = client.images.generate(
    model="dall-e-2",
    prompt=prompt,
    size="256x256",
    quality="standard",
    n=1,
  )
  return response.data[0].url

col1, col2, col3 = st.columns(3)

with st.form("form"):
  prompt = st.text_area("Was solls denn werden?",placeholder="Gib hier deinen Prompt ein...")
  if st.form_submit_button("Zeig her!"):
    with st.spinner("Wird gemacht..."):
      st.session_state.image_url = create_image(prompt)
    st.session_state.prompt = prompt
    with col2:
        st.image(st.session_state.image_url)
        if st.session_state.image_url not in st.session_state.image_list:
          st.session_state.image_list.insert(0, [st.session_state.image_url, st.session_state.prompt])
        st.markdown(f"***{st.session_state.prompt}***")



#if st.session_state.image_url != "":

      #pic_count = 0
    #st.markdown("""---""")
#    for picture in st.session_state.image_list:
#      if picture[0] != st.session_state.image_url:
#        pic_count += 1
#        pic_count_name = f"share_pic{pic_count}"
#        with st.form(pic_count_name):
#          st.image(picture[0])
#          st.markdown(f"***{picture[1]}***")
#          if st.form_submit_button("In der Galerie teilen"):
#            st.session_state.image = ({"image_url": picture[0],
#                                       "prompt": picture[1]})
#            if db.add_image(st.session_state.image) == False:
#              st.error("Das Bild ist schon in der Galerie.")
#            else:
#              st.success('Alles klaro...Dein Bild kann jetzt in der Galerie bewundert werden.')