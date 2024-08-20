import streamlit as st
from openai import OpenAI
import pw_check as pw
import requests
from datetime import datetime

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

nextcloud_url = st.secrets["NC_URL"]
username = st.secrets["NC_user"]
password = st.secrets["NC_pw"]
nc_folder = "pic_uploads"

st.markdown(f"> 🎨")
with st.expander("Wie geht das hier?"):
  st.markdown("Hier ist der Ort, an dem du aus Text Bilder machen kannst. Gibt unten deinen Prompt ein, Klicke auf \"Zeig\' her\" und lasse dich überraschen.")
  st.markdown("Möchtest du ein Bild teilen, klicke auf \"Bild mit dem Kurs teilen\". **Alle Bilder, die nicht geteilt wurden, verschwinden, sobald du die Seite verlässt oder ein anderes Bild erzeugst.**")
  st.markdown("Alle geteilten Bilder findest du unter https://share.olatu.de/index.php/s/ZR56mXYbHTXd5rq")
st.title("Let`s draw.")


def create_image(prompt):
  response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
      "authorization": st.secrets["SD_API_KEY"],
      "accept": "image/*"
    },
    files={"none": ''},
    data={
      "prompt": prompt,
      "output_format": "jpeg",
    },
  )

  if response.status_code == 200:
    print("Bild erfolgreich erstellt!")
    return response.content
  if response.status_code == 422:
    return 422
  else:
    raise Exception("Fehler beim Erstellen des Bildes: " + str(response.json))

def store_pic(image_content, nextcloud_url, nc_folder, username, password):
    folder_path = nc_folder
    # Aktuelles Datum und Uhrzeit abrufen
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"generated_image_{current_datetime}.jpg"
    full_path = f"{folder_path}/{file_name}"

    # Sende die Datei an Nextcloud
    response = requests.put(
      f"{nextcloud_url}/remote.php/webdav/{full_path}",
      auth=(username, password),
      data=image_content
    )
    print(response)

    # Überprüfe, ob der Upload erfolgreich war
    if response.status_code == 201:
      share_response = requests.post(
        f"{nextcloud_url}/ocs/v2.php/apps/files_sharing/api/v1/shares",
        auth=(username, password),
        headers={
          "OCS-APIRequest": "true"
        },
        data={
          "path": f"/{full_path}",
          "shareType": 3,  # 3 steht für öffentlichen Link
          "permissions": 1  # 1 steht für nur Lesen
        }
      )
      print("Upload erfolgreich!")
      if share_response.status_code == 200:
        print(response.url)
      else:
        raise Exception("Fehler beim Erstellen des öffentlichen Links: " + str(share_response))
    else:
      print("Antwort der Nextcloud-API:", response.content)
      raise Exception("Fehler beim Hochladen des Bildes: " + str(response.content))

col1, col2, col3 = st.columns(3)

with st.form("form"):
  prompt = st.text_area("Was solls denn werden?",placeholder="Gib hier deinen Prompt ein...")
  if st.form_submit_button("Zeig her!"):
    st.session_state.prompt = prompt
    with st.spinner("Wird gemacht..."):
      st.session_state.image_url = create_image(prompt)
      if st.session_state.image_url == 422:
        st.markdown(
          "Stable Diffusion spricht nur Englisch :) Schreibe deinen Prompt bitte in englischer Sprache und probiere es nochmal.")
      else:
        st.image(st.session_state.image_url)

if st.button("Bild mit dem Kurs teilen"):
  if "prompt" not in st.session_state:
    st.markdown("Es gibt noch kein Bild, das geteilt werden könnte. Erstelle zunächst eines, indem du oben einen Prompt eingibst.")
  else:
    with st.spinner("Upload..."):
      store_pic(st.session_state.image_url, nextcloud_url, nc_folder, username, password)
      st.markdown("TipTop...Dein Bild ist in die Galerie geladen.")
      st.markdown(
        "Du findest alle vom Kurs erstellten Bilder hier: https://share.olatu.de/index.php/s/ZR56mXYbHTXd5rq")
      st.image(st.session_state.image_url)