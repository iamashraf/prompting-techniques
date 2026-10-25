"""Minimal call to a local Ollama server -- shared by every technique.

Deliberately not a multi-provider abstraction (no Claude/OpenAI support
here): this repo only needed Ollama so far, and a provider abstraction
with one real implementation is premature. Extract further if/when a
technique actually needs a second provider.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3.1:8b"


def ask_ollama(
    system: str | None,
    user: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.0,
    format: dict | str | None = None,
    max_tokens: int | None = None,
    top_p: float | None = None,
) -> str:
    print(f"--- sending to {model} (temperature={temperature}) ---")
    if system is not None:
        print(f"[system]\n{system}\n")
    print(f"[user]\n{user}\n")

    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    options = {"temperature": temperature}
    if max_tokens is not None:
        options["num_predict"] = max_tokens  # Ollama's name for max_tokens
    if top_p is not None:
        options["top_p"] = top_p

    payload = {
        "model": model,
        "messages": messages,
        "options": options,
        "stream": False,
    }
    if format is not None:
        payload["format"] = format

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["message"]["content"]
