from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup


def load_plain_text(file_path: str) -> str:
    """
    Lê arquivos TXT, MD, TEX, HTML e HTM.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    text = path.read_text(encoding="utf-8", errors="ignore")

    if path.suffix.lower() in [".html", ".htm"]:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text("\n").strip()

    return text.strip()