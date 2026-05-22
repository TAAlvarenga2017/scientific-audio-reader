from __future__ import annotations

from pathlib import Path


class LatexOCR:
    """
    OCR matemático para converter imagem de fórmula em LaTeX.

    Esta classe tenta usar pix2tex.
    Se pix2tex não estiver instalado, retorna marcador de falha.
    """

    def __init__(self):
        self.model = None
        self.available = False

        try:
            from pix2tex.cli import LatexOCR as Pix2TexOCR

            self.model = Pix2TexOCR()
            self.available = True
        except Exception:
            self.model = None
            self.available = False

    def image_to_latex(self, image_path: str) -> str:
        path = Path(image_path)

        if not path.exists():
            return "[imagem matemática não encontrada]"

        if not self.available:
            return "[OCR matemático indisponível: instale pix2tex]"

        try:
            from PIL import Image

            img = Image.open(path)
            latex = self.model(img)

            if latex:
                return latex.strip()

            return "[expressão matemática não reconhecida por OCR]"

        except Exception as e:
            return f"[erro no OCR matemático: {e}]"