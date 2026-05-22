from __future__ import annotations

from pathlib import Path

from core.document_readers.docx_reader import load_docx_text
from core.document_readers.pdf_reader import load_pdf_text
from core.document_readers.text_reader import load_plain_text

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".tex",
    ".html",
    ".htm",
}


def load_document_text(file_path: str, max_pages: int | None = None) -> str:
    """
    Carrega texto de diferentes formatos.

    Para DOCX:
        prioriza Pandoc para preservar equações como LaTeX.

    Para PDF:
        usa PyMuPDF.

    Para TXT, MD, TEX, HTML:
        lê texto diretamente.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Formato não suportado: {suffix}. "
            f"Formatos suportados: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if suffix == ".docx":
        return load_docx_text(str(path))

    if suffix == ".pdf":
        return load_pdf_text(str(path), max_pages=max_pages)

    return load_plain_text(str(path))