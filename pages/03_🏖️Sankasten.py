import streamlit as st
import html

import db
import pw_check as pw
import chat_ui

#Passwort checken
if pw.check_password() == False:
    st.stop()  # Do not continue if check_password is not True.

# Inject modern chat UI CSS
chat_ui.inject_chat_css()

# Add custom styling for bot cards
st.markdown("""
    <style>
    /* Style for bordered containers (bot cards) */
    div[data-testid="stContainer"] > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border-left: 4px solid #667eea !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def get_model_emoji(model):
    """Returns an emoji based on model type"""
    if "gpt-4o" in model or "gpt-4.1" in model:
        return "🚀"
    elif "claude" in model:
        return "🧠"
    elif "mini" in model or "nano" in model:
        return "⚡"
    else:
        return "🤖"

def get_temp_description(temp):
    """Returns a description for temperature value"""
    if temp <= 0.3:
        return "Präzise"
    elif temp <= 0.7:
        return "Ausgewogen"
    else:
        return "Kreativ"

def render_bot_card(bot, name):
    """Renders a modern card for each bot"""
    bot_name = bot["bot_name"]
    sys_prompt = bot["sys_prompt"]
    temp = bot["temp"]
    model = bot["model"]

    # Truncate long prompts for preview
    prompt_preview = sys_prompt[:100] + "..." if len(sys_prompt) > 100 else sys_prompt

    # Use Streamlit's container with border styling
    with st.container(border=True):
        # Header with bot name and model badge
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🤖 {bot_name}")
        with col2:
            st.markdown(f"**{get_model_emoji(model)}** `{model}`")

        # Prompt preview - using plain italic text
        st.markdown(f"*{prompt_preview}*")

        st.markdown("")  # spacing

        # Temperature info
        st.markdown(f"🌡️ **Temperature:** {temp} ({get_temp_description(temp)})")

        # Actions row
        col1, col2 = st.columns([3, 1])

        with col1:
            with st.expander("📋 Details anzeigen"):
                st.markdown("**Vollständiger Systemprompt:**")
                st.code(sys_prompt, language=None)
                st.markdown(f"**Modell:** {model}")
                st.markdown(f"**Temperature:** {temp} ({get_temp_description(temp)})")

        with col2:
            if st.button("🎲 Ausprobieren", key=f"try_{name}", use_container_width=True):
                st.session_state["bot"] = db.search_bot(name)
                st.session_state["bot_name"] = st.session_state.bot["bot_name"]
                st.session_state["sys_prompt"] = st.session_state.bot["sys_prompt"]
                st.session_state.messages = [{"role": "system", "content": st.session_state.sys_prompt}]
                st.session_state["model"] = st.session_state.bot["model"]
                st.session_state["temp"] = st.session_state.bot["temp"]
                chat_ui.show_success_message(f'**{bot_name}** geladen! Gehe zum Spielplatz, um ihn zu testen.')

# Streamlit UI
def main():
    # Modern header
    chat_ui.display_chat_header(
        bot_name="Sandkasten",
        description="🏖️ Entdecke und teile Bot-Konfigurationen mit der Community"
    )

    with st.expander("ℹ️ So funktioniert der Sandkasten", False):
        st.markdown("**Teilen:** Hast du auf dem Spielplatz eine spannende Bot-Rolle erstellt? "\
                    "Klicke dort auf \"Bot im Sandkasten teilen\" und lass andere daran teilhaben.")
        st.markdown("**Entdecken:** Durchstöbere die geteilten Bots unten und probiere sie aus. "\
                    "Klicke auf \"Ausprobieren\" und wechsle dann zum Spielplatz.")
        st.markdown("**Experimentieren:** Du kannst nichts kaputt machen - probiere einfach aus! 😊")

    st.markdown("---")

    # Get all bots
    bot_names = db.get_all_bot_names()

    if not bot_names:
        chat_ui.show_info_message("Noch keine Bots im Sandkasten. Sei der Erste und teile einen Bot!")
        return

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filter & Suche")

        # Search
        search_term = st.text_input("Bot suchen", placeholder="Name eingeben...")

        # Model filter
        all_models = list(set([db.search_bot(name)["model"] for name in bot_names]))
        selected_models = st.multiselect(
            "Nach Modell filtern",
            options=all_models,
            default=all_models
        )

        # Temperature filter
        temp_range = st.slider(
            "Temperature-Bereich",
            0.0, 1.0, (0.0, 1.0),
            help="Filtere Bots nach ihrer Temperature-Einstellung"
        )

        # Sort options
        sort_by = st.selectbox(
            "Sortieren nach",
            ["Name (A-Z)", "Name (Z-A)", "Modell", "Temperature"]
        )

        st.markdown("---")
        st.markdown(f"**{len(bot_names)}** Bots im Sandkasten")

    # Filter and sort bots
    filtered_bots = []
    for name in bot_names:
        bot = db.search_bot(name)

        # Apply filters
        if search_term and search_term.lower() not in bot["bot_name"].lower():
            continue
        if bot["model"] not in selected_models:
            continue
        if not (temp_range[0] <= bot["temp"] <= temp_range[1]):
            continue

        filtered_bots.append((name, bot))

    # Apply sorting
    if sort_by == "Name (A-Z)":
        filtered_bots.sort(key=lambda x: x[1]["bot_name"].lower())
    elif sort_by == "Name (Z-A)":
        filtered_bots.sort(key=lambda x: x[1]["bot_name"].lower(), reverse=True)
    elif sort_by == "Modell":
        filtered_bots.sort(key=lambda x: x[1]["model"])
    elif sort_by == "Temperature":
        filtered_bots.sort(key=lambda x: x[1]["temp"])

    # Display results
    if not filtered_bots:
        chat_ui.show_info_message("Keine Bots gefunden, die deinen Filterkriterien entsprechen.")
    else:
        st.markdown(f"### 🤖 Verfügbare Bots ({len(filtered_bots)})")

        # Render bot cards
        for name, bot in filtered_bots:
            render_bot_card(bot, name)

if __name__ == "__main__":
    main()
