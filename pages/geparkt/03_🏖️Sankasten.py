import streamlit as st

import db
import pw_check as pw

#Passwort checken
if pw.check_password() == False:
    st.stop()  # Do not continue if check_password is not True.


# Streamlit UI
def main():
    st.markdown("> 🏖️")
    with st.expander("**Im Sandkasten wird das Spielzeug geteilt.**", True):
        st.markdown("Hast du deinem Bot auf dem *Spielplatz* eine spannende Rolle verpasst? "\
                    "Klicke auf dem Spielplatz in der Navigationsleite ganz unten auf \"Prompt im Sandkasten teilen\" und lasse die anderen daran teilhaben.")
        st.markdown("Umgedreht kannst du mit einem Klick auf die hier geteilten Bots die Entdeckungen der Anderen testen.")
        st.markdown("Schau doch mal durch die Liste unten und probier es einfach aus...du kannst nichts kaputt machen ;)")

    st.divider()

    # Anzeige der vorhandenen Prompts als Buttons
    bot_names = db.get_all_bot_names()
    for name in bot_names:
        #with st.expander("Einstellungen zeigen"):
        bot = db.search_bot(name)
        bot_name = bot["bot_name"]
        sys_prompt = bot["sys_prompt"]
        temp = bot["temp"]
        model = bot["model"]
        st.markdown(f"Botname: ***{bot_name}***")
        st.markdown(f"Systemprompt: *{sys_prompt}*")
        st.markdown(f"Temperature: *{temp}*")
        st.markdown(f"Modell: *{model}*")

        if st.button(f"**{name}** ausprobieren"):
            st.session_state["bot"] = db.search_bot(name)
            st.session_state["bot_name"] = st.session_state.bot["bot_name"]
            st.session_state["sys_prompt"] = st.session_state.bot["sys_prompt"]
            st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
            st.session_state["model"] = st.session_state.bot["model"]
            st.session_state["temp"] = st.session_state.bot["temp"]
            st.success('Ist eingeloggt. Gehe zum "Spielplatz", um die neue Rolle für deinen Bot zu testen. Viel Spaß!')

        st.markdown("""---""")

if __name__ == "__main__":
    main()
