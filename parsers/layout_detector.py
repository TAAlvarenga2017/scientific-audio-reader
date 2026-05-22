from __future__ import annotations
import re

TABLE_TERMS = [
    "total", "tratamentos", "blocos", "fv", "gl",
    "sq", "qm", "fc", "p-valor", "cultivares", "dose"
]

MATH_SYMBOLS = [
    "∑", "√", "β", "σ", "μ", "ε", "τ", "π", "≈", "≤", "≥", "≠",
    "∂", "̂", "^", "log(", "exp(", "argmin", "argmax", "N(", "X'", "ŷ"
]

def looks_like_table(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return False

    tabular_hits = 0
    for line in lines[:10]:
        if any(re.search(rf"\b{re.escape(term)}\b", line, re.IGNORECASE) for term in TABLE_TERMS):
            tabular_hits += 1
        if len(re.findall(r"\d+[,.]?\d*", line)) >= 3:
            tabular_hits += 1
    return tabular_hits >= 3

def looks_like_equation(text: str) -> bool:
    compact = " ".join(text.split())
    if not compact:
        return False

    hits = sum(1 for symbol in MATH_SYMBOLS if symbol in compact)
    if re.search(r"=\s*.*", compact) and hits >= 1:
        return True
    return hits >= 3
