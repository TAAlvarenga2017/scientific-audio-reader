from __future__ import annotations

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
TEXT_MODEL = "qwen2.5"

FORMULA_PROMPT = """
Converta a expressão matemática abaixo para leitura oral em português do Brasil.

Regras obrigatórias:
- Preserve fielmente a estrutura matemática.
- NÃO explique.
- NÃO resuma.
- NÃO omita símbolos relevantes.
- Apenas transforme notação em fala.
- Use convenções orais simples, por exemplo:
  x̄ -> x barra
  μ -> mi
  Σ⁻¹ -> sigma inversa
  ' -> transposto
  ∑ -> somatório
  |Σ| -> determinante de sigma
  ℝ^p -> espaço real de dimensão p

Expressão:
{content}
"""

TEXT_PROMPT = """
Reescreva o trecho abaixo para leitura em voz em português do Brasil.

Regras:
- Preserve o conteúdo.
- Corrija apenas pequenas quebras de PDF.
- Não invente nada.
- Não resuma.

Trecho:
{content}
"""

TABLE_PROMPT = """
Converta a tabela abaixo para leitura em voz em português do Brasil.

Regras:
- Preserve a fidelidade dos dados.
- Se a tabela for extensa, mantenha o cabeçalho e descreva as linhas de forma organizada.
- Não invente valores.
- Não explique além do necessário para permitir leitura compreensível.

Tabela:
{content}
"""


class QwenVerbalizer:
    def __init__(self, model: str = TEXT_MODEL, url: str = OLLAMA_URL):
        self.model = model
        self.url = url

    def _generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        resp = requests.post(self.url, json=payload, timeout=300)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()

    def verbalize_block(self, block: dict) -> str:
        block_type = block.get("type", "text")
        content = block.get("content", "").strip()

        if not content:
            return ""

        if block_type == "formula":
            return self._generate(FORMULA_PROMPT.format(content=content))

        if block_type == "table":
            return self._generate(TABLE_PROMPT.format(content=content))

        if block_type == "reference":
            return ""

        return self._generate(TEXT_PROMPT.format(content=content))
