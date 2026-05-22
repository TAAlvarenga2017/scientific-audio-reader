from __future__ import annotations

from pathlib import Path
import pymupdf


def load_pdf_text(pdf_path: str, max_pages: int | None = None) -> str:
    """
    Extrai texto de PDF usando PyMuPDF.

    Observação:
    PDFs com fórmulas, gráficos ou tabelas complexas podem perder parte
    da estrutura matemática. A etapa de OCR matemático deve ser usada
    posteriormente para fórmulas como imagem.
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    doc = pymupdf.open(str(path))
    chunks: list[str] = []

    total_pages = len(doc)
    pages_to_read = total_pages if max_pages is None else min(max_pages, total_pages)

    for i in range(pages_to_read):
        page = doc[i]
        text = page.get_text("text")

        if text and text.strip():
            chunks.append(text.strip())

    doc.close()

    return "\n\n".join(chunks).strip()