from pathlib import Path
import requests
import base64


class LlavaParser:
    def __init__(self, model="llava:7b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def _encode_image(self, image_path: Path) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def parse_page_image(self, image_path: Path) -> str:
        image_base64 = self._encode_image(image_path)

        prompt = """
Leia esta página de um documento científico.

REGRAS:
- NÃO resuma
- NÃO omita conteúdo
- Leia fórmulas matemáticas corretamente
- Preserve a ordem da leitura
- Transforme tudo em texto falado

Exemplo:
(x̄ − μ)' Σ⁻¹ (x̄ − μ)
→ x barra menos mi transposto vezes sigma inversa vezes x barra menos mi
"""

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
            },
        )

        response.raise_for_status()
        return response.json()["response"]