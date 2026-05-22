from __future__ import annotations
import re
from parsers.layout_detector import looks_like_equation, looks_like_table

REFERENCE_PATTERNS = [
    r"^refer[eê]ncias",
    r"\bdoi\b",
    r"\bet al\.\b",
]

TITLE_PATTERNS = [
    r"^tema\s+\d+",
    r"^\d+(\.\d+)*\s*[-–]?\s*[A-Za-zÀ-ÿ]",
]

def classify_block_type(text: str) -> tuple[str, float]:
    compact = " ".join(text.split())
    lower = compact.lower()

    if not compact:
        return "unknown", 0.0

    if looks_like_table(text):
        return "table", 0.92

    if looks_like_equation(text):
        return "equation", 0.90

    if any(re.search(pattern, lower, re.IGNORECASE) for pattern in REFERENCE_PATTERNS):
        return "reference", 0.88

    if len(compact) < 180 and any(re.search(pattern, compact, re.IGNORECASE) for pattern in TITLE_PATTERNS):
        return "title", 0.84

    return "text", 0.65
