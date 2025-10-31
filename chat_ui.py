"""
Modern Chat UI Components for ErgoMaite25
Provides consistent, professional chat interface styling across all pages
"""

import streamlit as st
from datetime import datetime

def inject_chat_css():
    """Injects custom CSS for modern chat interface"""
    st.markdown("""
    <style>
    /* Main chat container */
    .stChatMessage {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }

    .stChatMessage:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* User messages - right aligned with distinct color */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 10%;
    }

    .stChatMessage[data-testid="user-message"] p {
        color: white !important;
    }

    /* Assistant messages - left aligned with neutral color */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
        color: #2c3e50;
        margin-right: 10%;
        border-left: 4px solid #667eea;
    }

    /* Chat input styling */
    .stChatInputContainer {
        border-top: 2px solid #e9ecef;
        padding-top: 1rem;
        margin-top: 1rem;
        background: transparent !important;
    }

    /* Target the chat input wrapper */
    .stChatInputContainer > div {
        background: transparent !important;
    }

    /* Style the actual input field */
    .stChatInputContainer textarea {
        border-radius: 24px !important;
        border: 2px solid #e9ecef !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    .stChatInputContainer textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }

    /* Remove any extra padding/margin from wrapper divs */
    .stChatInputContainer > div > div {
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
    }

    /* Message content */
    .stChatMessage p {
        line-height: 1.6;
        font-size: 1rem;
    }

    /* Code blocks in messages */
    .stChatMessage code {
        background: rgba(0, 0, 0, 0.05);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
    }

    .stChatMessage pre {
        background: rgba(0, 0, 0, 0.05);
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
    }

    /* Avatar styling */
    .stChatMessage img {
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Loading indicator */
    .chat-loading {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: #f5f7fa;
        border-radius: 12px;
        margin: 0.5rem 0;
    }

    .chat-loading-dot {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: loading-bounce 1.4s infinite ease-in-out;
    }

    .chat-loading-dot:nth-child(1) {
        animation-delay: -0.32s;
    }

    .chat-loading-dot:nth-child(2) {
        animation-delay: -0.16s;
    }

    @keyframes loading-bounce {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }

    /* Bot name badge */
    .bot-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }

    /* Message timestamp */
    .message-timestamp {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.25rem;
        font-style: italic;
    }

    /* Error messages */
    .error-message {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #c92a2a;
    }

    /* Success messages */
    .success-message {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #2f9e44;
    }

    /* Info messages */
    .info-message {
        background: linear-gradient(135deg, #4dabf7 0%, #339af0 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #1971c2;
    }

    /* Smooth scroll for chat container */
    .main .block-container {
        scroll-behavior: smooth;
    }

    /* Copy button styling */
    .copy-button {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
        float: right;
    }

    .copy-button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
    }

    /* Model indicator badge */
    .model-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }

    /* Expander styling for better integration */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        border: 1px solid #dee2e6;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        border-color: #667eea;
    }

    /* Sidebar improvements */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }

    /* Button styling improvements */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        border: 2px solid transparent;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Primary action buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Chat header styling */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
    }

    .chat-header h3 {
        color: white;
        margin: 0;
        font-size: 1.5rem;
    }

    .chat-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)


def display_chat_header(bot_name, model=None, description=None):
    """
    Displays a modern chat header with bot information

    Args:
        bot_name: Name of the bot
        model: Optional model name to display
        description: Optional bot description
    """
    model_badge = f'<span class="model-badge">{model}</span>' if model else ''
    desc_text = f'<p>{description}</p>' if description else ''

    st.markdown(f"""
    <div class="chat-header">
        <h3>💬 {bot_name} {model_badge}</h3>
        {desc_text}
    </div>
    """, unsafe_allow_html=True)


def display_message_with_timestamp(role, content, timestamp=None):
    """
    Displays a chat message with modern styling and optional timestamp

    Args:
        role: Message role (user/assistant)
        content: Message content
        timestamp: Optional timestamp (defaults to current time)
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")

    with st.chat_message(role):
        st.markdown(content)
        st.markdown(f'<div class="message-timestamp">{timestamp}</div>', unsafe_allow_html=True)


def show_loading_indicator(message="Denkt nach..."):
    """
    Shows a modern loading indicator

    Args:
        message: Loading message to display
    """
    return st.markdown(f"""
    <div class="chat-loading">
        <div class="chat-loading-dot"></div>
        <div class="chat-loading-dot"></div>
        <div class="chat-loading-dot"></div>
        <span style="margin-left: 0.5rem; color: #667eea; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def show_error_message(message):
    """Displays a styled error message"""
    st.markdown(f"""
    <div class="error-message">
        <strong>⚠️ Fehler:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def show_success_message(message):
    """Displays a styled success message"""
    st.markdown(f"""
    <div class="success-message">
        <strong>✓</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def show_info_message(message):
    """Displays a styled info message"""
    st.markdown(f"""
    <div class="info-message">
        <strong>ℹ️</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def get_avatar(role):
    """
    Returns appropriate avatar emoji for role

    Args:
        role: Message role (user/assistant/teacher/system)

    Returns:
        Avatar emoji string
    """
    avatars = {
        "user": "👤",
        "assistant": "🤖",
        "teacher": "🎓",
        "system": "⚙️"
    }
    return avatars.get(role, "💬")


def display_modern_chat_messages(messages, show_system=False):
    """
    Displays chat messages with modern styling

    Args:
        messages: List of message dicts with 'role' and 'content'
        show_system: Whether to show system messages (default: False)
    """
    for message in messages:
        role = message["role"]
        content = message["content"]

        # Skip system messages unless explicitly requested
        if role == "system" and not show_system:
            continue

        avatar = get_avatar(role)
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)


def create_chat_input_with_placeholder(placeholder="Lass' mal reden.", key=None):
    """
    Creates a styled chat input with custom placeholder

    Args:
        placeholder: Placeholder text
        key: Optional unique key for the input

    Returns:
        User input or None
    """
    return st.chat_input(placeholder, key=key)
