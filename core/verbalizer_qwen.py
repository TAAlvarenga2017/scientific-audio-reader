from __future__ import annotations

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
TEXT_MODEL = "qwen2.5:latest"


FORMULA_PROMPT = """
Converta a expressão matemática abaixo para leitura oral fiel em português do Brasil.

Regras obrigatórias:
- NÃO explique.
- NÃO resuma.
- NÃO omita termos.
- Preserve a estrutura matemática.
- Apenas transforme a notação em fala.
- Leia símbolos matemáticos de forma natural.

Convenções:
𝛽 -> beta
𝛽̂ -> beta chapéu
𝜀 -> épsilon
𝜎 -> sigma
𝜎2 -> sigma ao quadrado
𝜇 -> mi
∑ -> somatório
∏ -> produtório
𝑥̄ -> x barra
𝑦̂ -> y chapéu
′ -> transposto
− -> menos
× -> vezes
/ -> dividido por
= -> igual a
𝑛 -> n
𝑖 -> i

Expressão:
{content}

Retorne somente a leitura oral da expressão.
"""


class QwenVerbalizer:
    def __init__(self, model: str = TEXT_MODEL, url: str = OLLAMA_URL):
        self.model = model
        self.url = url

    def _generate(self, prompt: str) -> str:
        try:
            resp = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=300,
            )

            if resp.status_code != 200:
                return ""

            return resp.json().get("response", "").strip()

        except Exception:
            return ""

    def verbalize_block(self, block: dict) -> str:
        content = block.get("content", "").strip()
        block_type = block.get("type", "text")

        if not content:
            return ""

        if block_type == "formula":
            return self._generate(FORMULA_PROMPT.format(content=content))

        return content