"""A minimal ChatGPT-style chat UI for a local LLM.

Uses the OpenAI Python client against Ollama's OpenAI-compatible API,
with Gradio for the web interface.
"""

import os

import gradio as gr
from openai import OpenAI

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")

# Ollama ignores the API key, but the OpenAI client requires one to be set.
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def chat(message, history):
    """Stream a reply from the local model, given the new message and chat history."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
        )
        reply = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                yield reply
    except Exception as exc:
        yield (
            f"⚠️ Could not reach the model `{MODEL_NAME}` at {OLLAMA_BASE_URL}.\n\n"
            f"Make sure Ollama is running and the model is pulled "
            f"(`ollama pull {MODEL_NAME}`).\n\nError: {exc}"
        )


demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="Local Chat",
    description=f"Chat with **{MODEL_NAME}** running locally via Ollama.",
    examples=[
        "Explain what a large language model is in simple terms.",
        "Write a Python function that reverses a string.",
        "Give me three ideas for a weekend project.",
    ],
)


if __name__ == "__main__":
    demo.launch()
