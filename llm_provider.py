"""
LLM Provider abstraction layer
Automatically routes to OpenAI or Anthropic based on model name
"""
import streamlit as st
from openai import OpenAI
from anthropic import Anthropic

# Client singletons
_openai_client = None
_anthropic_client = None

def get_provider(model_name):
    """
    Determine which provider to use based on model name
    Returns: 'openai' or 'anthropic'
    """
    if model_name.startswith('claude'):
        return 'anthropic'
    else:
        return 'openai'

def call_llm(model, temperature, messages):
    """
    Unified LLM call that automatically routes to the correct provider

    Args:
        model: Model name (e.g., 'gpt-4o' or 'claude-3-5-sonnet-20241022')
        temperature: Temperature setting (0.0-1.0)
        messages: List of message dicts with 'role' and 'content'

    Returns:
        String response from the model
    """
    provider = get_provider(model)

    if provider == 'anthropic':
        return _call_anthropic(model, temperature, messages)
    else:
        return _call_openai(model, temperature, messages)

def _get_openai_client():
    """Get or create OpenAI client singleton"""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    return _openai_client

def _get_anthropic_client():
    """Get or create Anthropic client singleton"""
    global _anthropic_client
    if _anthropic_client is None:
        import httpx
        # Create a custom httpx client without proxy support to avoid compatibility issues
        http_client = httpx.Client(
            timeout=httpx.Timeout(60.0, read=300.0),
            follow_redirects=True,
        )
        _anthropic_client = Anthropic(
            api_key=st.secrets["ANTHROPIC_API_KEY"],
            http_client=http_client
        )
    return _anthropic_client

def _call_openai(model, temperature, messages):
    """Call OpenAI API"""
    client = _get_openai_client()
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

def _call_anthropic(model, temperature, messages):
    """
    Call Anthropic API
    Converts OpenAI-style messages to Anthropic format
    """
    client = _get_anthropic_client()

    # Separate system message from conversation messages
    system_message = None
    conversation_messages = []

    for msg in messages:
        if msg["role"] == "system":
            system_message = msg["content"]
        else:
            conversation_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # Build the API call
    kwargs = {
        "model": model,
        "temperature": temperature,
        "max_tokens": 4096,
        "messages": conversation_messages
    }

    if system_message:
        kwargs["system"] = system_message

    response = client.messages.create(**kwargs)
    return response.content[0].text
