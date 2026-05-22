from __future__ import annotations
import unicodedata
import re

def safe_filename(name: str) -> str:
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return text or "arquivo"
