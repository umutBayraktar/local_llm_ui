# local_llm_ui — Local LLM Chat

A very simple ChatGPT-style chat app that runs entirely on your machine.

- **Model:** [Llama 3.2](https://ollama.com/library/llama3.2) served by [Ollama](https://ollama.com)
- **Client:** the official [OpenAI Python library](https://github.com/openai/openai-python), pointed at Ollama's OpenAI-compatible API
- **UI:** [Gradio](https://www.gradio.app) chat interface with streaming replies

## Prerequisites

- Python 3.10+
- Ollama installed and running — download it from https://ollama.com/download

## Getting started

1. **Pull the model**

   ```bash
   ollama pull llama3.2
   ```

   Make sure Ollama is running (`ollama serve`, or just open the Ollama app).

2. **Clone the repo and create a virtual environment**

   ```bash
   git clone https://github.com/umutBayraktar/local_llm_ui.git
   cd local_llm_ui
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   python app.py
   ```

   Open http://127.0.0.1:7860 in your browser and start chatting.

## Configuration

You can override the defaults with environment variables:

| Variable          | Default                       | Description                          |
| ----------------- | ----------------------------- | ------------------------------------ |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1`   | Ollama's OpenAI-compatible endpoint  |
| `MODEL_NAME`      | `llama3.2`                    | Any model you have pulled in Ollama  |
| `SYSTEM_PROMPT`   | `You are a helpful assistant.`| System message sent with every chat  |

Example:

```bash
MODEL_NAME=llama3.2:1b python app.py
```

## How it works

Ollama exposes an OpenAI-compatible endpoint at `/v1`, so the standard OpenAI client works by just changing `base_url`:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # key is ignored
```

`app.py` sends the full conversation history on each turn and streams the response token by token into a Gradio `ChatInterface`.

## Troubleshooting

- **Connection error** — Ollama isn't running. Start it with `ollama serve`.
- **Model not found** — run `ollama pull llama3.2`.
