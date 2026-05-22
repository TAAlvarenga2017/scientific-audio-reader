from __future__ import annotations

import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
VISION_MODEL = "qwen2.5vl"

SYSTEM_PROMPT = """
Você é um parser de documentos científicos em português do Brasil.
Analise a imagem de UMA página de documento e devolva SOMENTE um array JSON válido.

Formato de saída:
[
  {"type": "title", "content": "..."},
  {"type": "text", "content": "..."},
  {"type": "formula", "content": "..."},
  {"type": "table", "content": "..."},
  {"type": "list", "content": "..."},
  {"type": "reference", "content": "..."}
]

Regras:
- Preserve a ordem de leitura.
- Se encontrar fórmula, mantenha a fórmula fiel.
- Se encontrar tabela, preserve seu conteúdo textual do modo mais fiel possível.
- Não explique.
- Não resuma.
- Não invente conteúdo.
- Retorne SOMENTE o JSON.
"""


class QwenVLParser:
    def __init__(self, model: str = VISION_MODEL, url: str = OLLAMA_URL):
        self.model = model
        self.url = url

    def parse_page_image(self, image_path: str) -> list[dict]:
        payload = {
            "model": self.model,
            "prompt": SYSTEM_PROMPT,
            "images": [image_path],
            "stream": False,
        }
        resp = requests.post(self.url, json=payload, timeout=300)
        resp.raise_for_status()
        raw = resp.json().get("response", "").strip()

        # Tolerância a blocos markdown
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass

        # fallback conservador
        return [{"type": "text", "content": raw}]
