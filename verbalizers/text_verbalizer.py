from __future__ import annotations
import re

def normalize_scientific_text(text: str) -> str:
    text = text.replace("\x0c", "\n").replace("￾", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"\n", " ", text)
    return text.strip()

def verbalize_text_block(text: str, mode: str) -> str:
    text = normalize_scientific_text(text)

    replacements = {
        "ANOVA": "análise de variância",
        "ANAVA": "análise de variância",
        "MQO": "mínimos quadrados ordinários",
        "MV": "máxima verossimilhança",
        "MSE": "quadrado médio do erro",
        "RMSE": "raiz do quadrado médio do erro",
        "AIC": "critério de informação de Akaike",
        "BIC": "critério de informação Bayesiano",
    }

    for old, new in replacements.items():
        text = re.sub(rf"\b{re.escape(old)}\b", new, text, flags=re.IGNORECASE)

    text = re.sub(r"\bp-valor\b", "p valor", text, flags=re.IGNORECASE)
    text = re.sub(r"\bp\s*<\s*0,05\b", "p menor que zero vírgula zero cinco", text, flags=re.IGNORECASE)
    text = re.sub(r"\bp\s*>\s*0,05\b", "p maior que zero vírgula zero cinco", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(\d+),(\d+)\b", r"\1 vírgula \2", text)
    text = re.sub(r"\b(\d+)%(?!\w)", r"\1 por cento", text)
    text = re.sub(r"\bkg/ha\b", "quilogramas por hectare", text, flags=re.IGNORECASE)
    text = re.sub(r"\bt/ha\b", "toneladas por hectare", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcm\b", "centímetros", text, flags=re.IGNORECASE)

    return text.strip()
