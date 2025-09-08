import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

class LocalLLM:
    def __init__(self, model=None, host=None):
        self.model = model or OLLAMA_MODEL
        self.host = (host or OLLAMA_HOST).rstrip("/")

    def generate(self, prompt: str) -> str:
        """Call Ollama locally (no streaming)."""
        url = f"{self.host}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "")
