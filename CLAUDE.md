# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ErgoMaite25 is a Streamlit-based educational platform for occupational therapy (Ergotherapie) that provides interactive AI-powered learning tools. The application is password-protected and uses both OpenAI GPT and Anthropic Claude models for conversational AI features, with MongoDB for data persistence.

## Key Architecture

### Application Structure
- **Start.py**: Main entry point with password protection and welcome page
- **pages/**: Multi-page Streamlit app with 5 distinct learning modules
  - 01_KIrussell.py: Main chatbot carousel with pre-configured bots
  - 02_Spielplatz.py: Playground for experimenting with custom bot configurations
  - 03_Sankasten.py: Sandbox for sharing and discovering community-created bots
  - 04_School-of-Prompting.py: Interactive prompting techniques learning module
  - 05_StaffelAI.py: Image generation module using Stability AI

### Core Modules
- **db.py**: MongoDB interface layer - all database operations go through this module
- **pw_check.py**: Centralized password authentication using Streamlit secrets
- **parameters.py**: Configuration parameters (initial bot settings)
- **llm_provider.py**: Multi-provider LLM abstraction layer for OpenAI and Anthropic APIs

### LLM Provider Abstraction
The application uses a unified interface for calling both OpenAI and Anthropic models through `llm_provider.py`:

**Automatic Provider Detection**
- Models starting with 'claude' → Anthropic API
- All other models → OpenAI API

**Supported Models (2025)**
- OpenAI: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini
- Anthropic: claude-sonnet-4-5-20250929, claude-haiku-4-5-20251001, claude-3-5-haiku-20241022

**Key Features**
- `call_llm(model, temperature, messages)`: Unified interface for all LLM calls
- Automatic message format conversion (Anthropic requires separate system messages)
- Client singleton pattern for efficient resource management
- Custom httpx client for Anthropic to avoid proxy configuration issues

**Implementation Details**
```python
# All pages use the same interface
import llm_provider

full_response = llm_provider.call_llm(
    model=st.session_state["model"],
    temperature=st.session_state["temp"],
    messages=st.session_state["messages"]
)
```

### Data Flow Pattern
1. All pages check password via `pw_check.check_password()` before rendering
2. Bot configurations stored in MongoDB (ErgoMaite.Bots, ErgoMaite.Sandkasten collections)
3. Session state manages bot configuration across page navigation
4. Feedback stored in separate Feedback.Messages collection

## MongoDB Schema

### Collections
- **ErgoMaite.Bots**: Curated bot configurations (active bots shown in KIrussell)
- **ErgoMaite.Sandkasten**: Community-shared bot configurations
- **ErgoMaite.Settings**: App settings (e.g., start page content)
- **ErgoMaite.Images**: Image metadata for shared images
- **Feedback.Bots**: Bot feedback schemas
- **Feedback.Messages**: User conversation feedback

### Bot Document Structure
```python
{
    "bot_name": str,
    "sys_prompt": str,
    "model": str,  # OpenAI (gpt-4.1, gpt-4o) or Anthropic (claude-sonnet-4-5-20250929)
    "model_if_error": str,  # fallback model
    "temp": float,  # 0.0-1.0
    "prefix": str | None,  # optional initial assistant message
    "injection": str | None,  # optional prompt injection
    "explanation_title": str | None,
    "explanation_text": str | None,
    "explanation_text_second": str | None,
    "active": bool  # only for ErgoMaite.Bots
}
```

## Session State Management

### Critical Session Variables
- **bot_name, sys_prompt, model, temp**: Current bot configuration
- **messages**: OpenAI chat history format (list of role/content dicts)
- **Komme_vom_Spielplatz**: Flag indicating navigation from Spielplatz to KIrussell
- **displayed_messages**: Separate message tracking for School-of-Prompting module
- **teacher_messages**: Feedback history in School-of-Prompting

### Navigation Pattern
When a bot is configured in Sankasten and user clicks "ausprobieren", it:
1. Stores bot config in session_state
2. Sets `Komme_vom_Spielplatz = True`
3. User navigates to Spielplatz page
4. Spielplatz detects flag and loads the selected bot

## Development Commands

### Running the Application
```bash
streamlit run Start.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Environment Configuration
Required secrets in `.streamlit/secrets.toml`:
- `password`: App password for pw_check
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key (for Claude models)
- `URI_MONGODB`: MongoDB connection string
- `SD_API_KEY`: Stability AI API key (for image generation)
- `NC_URL`, `NC_user`, `NC_pw`: Nextcloud credentials for image storage

## Error Handling Pattern

The codebase uses a three-tier retry pattern for LLM API calls (works with both OpenAI and Anthropic):
1. Try with configured model
2. On failure, wait 5 seconds and retry same model
3. On second failure, fallback to `model_if_error` (typically a cheaper/faster model)

This pattern appears in KIrussell.py and School-of-Prompting.py. The llm_provider abstraction layer handles provider-specific differences transparently.

## School-of-Prompting Module

This is the most complex module, teaching 5 prompting techniques through interactive exercises:
- Zero-Shot Prompting
- One-Shot Prompting
- Few-Shot Prompting
- Chain-of-Thought Prompting
- Skala Prompting

### Dual-Bot Architecture
Uses two separate bot instances:
- **Assistent**: Main conversational bot for exercises
- **Teacher**: Provides meta-feedback on user's prompting attempts

The Teacher bot analyzes the conversation history and current exercise to provide contextual feedback.

## Image Generation (StaffelAI)

- Uses Stability AI's Core model (v2beta endpoint)
- Images stored in Nextcloud with timestamped filenames
- Shared via Nextcloud public links
- Special "emotion card deck" feature with predefined feelings list
- Filename format: `{username}_{feeling}_{timestamp}.jpg`

## Code Conventions

### Import Pattern
```python
import streamlit as st
import db
import pw_check as pw
import parameters as par
import llm_provider  # For pages that use AI chatbot functionality
```

### Password Check (Always First)
```python
if pw.check_password() == False:
    st.stop()
```

### Message Display Pattern
```python
def display_input():
    for message in st.session_state.messages:
        if message["role"] == "system":
            pass
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
```

## Known Issues (from TODOs)

- db.py:4 - Connection closing strategy needs improvement
- KIrussell.py:88 - Injections not fully implemented
- KIrussell.py:191 - Conversation continuation issues
- Spielplatz.py:109 - Need to check for duplicate bot names/prompts
