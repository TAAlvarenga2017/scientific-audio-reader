from __future__ import annotations
import re

def verbalize_equation(text: str, mode: str) -> str:
    text = " ".join(text.split())
    spoken = simplify_math_for_speech(text)
    if mode == "Simples":
        return f"Expressão matemática: {spoken}"
    return spoken

def simplify_math_for_speech(text: str) -> str:
    replacements = {
        "β̂0": "beta zero estimado",
        "β̂1": "beta um estimado",
        "β̂2": "beta dois estimado",
        "β̂3": "beta três estimado",
        "β0": "beta zero",
        "β1": "beta um",
        "β2": "beta dois",
        "β3": "beta três",
        "σ²": "sigma ao quadrado",
        "σ2": "sigma ao quadrado",
        "μ": "mi",
        "ε": "épsilon",
        "τ": "tau",
        "π": "pi",
        "∑": "somatório",
        "√": "raiz quadrada de",
        "≤": "menor ou igual a",
        "≥": "maior ou igual a",
        "≠": "diferente de",
        "≈": "aproximadamente igual a",
        "∞": "infinito",
        "∂": "derivada parcial",
        "exp": "exponencial",
        "argmin": "argumento que minimiza",
        "argmax": "argumento que maximiza",
        "log": "logaritmo",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    rules = [
        (r"\bl\s*\(\s*sigma ao quadrado\s*\)", "função log verossimilhança de sigma ao quadrado"),
        (r"\bN\s*\(\s*0\s*,\s*sigma ao quadrado\s*\)", "distribuição normal com média zero e variância sigma ao quadrado"),
        (r"([A-Za-z])\^2", r"\1 ao quadrado"),
        (r"([A-Za-z])\^3", r"\1 ao cubo"),
        (r"\)\s*\^2", " tudo ao quadrado"),
        (r"\)\s*2", " tudo ao quadrado"),
        (r"\bn\s*/\s*2\b", "ene sobre dois"),
        (r"\b1\s*/\s*2\b", "um sobre dois"),
        (r"\b1\s*/\s*\(\s*2\s*sigma ao quadrado\s*\)", "um sobre duas vezes sigma ao quadrado"),
        (r"\bX'\b", "x transposto"),
        (r"\by'\b", "y transposto"),
        (r"\bX\s*'\s*X\b", "x transposto vezes x"),
        (r"\bX\s*'\s*y\b", "x transposto vezes y"),
    ]

    for pattern, repl in rules:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    text = re.sub(r"\by\s*i\b", "y i", text)
    text = re.sub(r"\bx\s*i\b", "x i", text)
    text = re.sub(r"\bi\s*=\s*1\b", "i igual a um", text)

    text = text.replace("=", " igual a ")
    text = text.replace("-", " menos ")
    text = text.replace("+", " mais ")
    text = text.replace("*", " vezes ")
    text = text.replace("/", " sobre ")
    text = text.replace("(", " abre parênteses ")
    text = text.replace(")", " fecha parênteses ")
    text = text.replace("²", " ao quadrado")
    text = text.replace("³", " ao cubo")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b2\s*pi\b", "dois pi", text, flags=re.IGNORECASE)

    return text.strip()
