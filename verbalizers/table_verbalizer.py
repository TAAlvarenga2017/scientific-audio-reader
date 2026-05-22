from __future__ import annotations
import re

def verbalize_table(text: str, mode: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    n_rows = len(lines)
    number_count = len(re.findall(r"\d+[,.]?\d*", text))

    if mode == "Simples":
        return (
            f"Tabela com {n_rows} linhas relevantes. "
            f"Foram detectados aproximadamente {number_count} valores numéricos. "
            f"Nesta versão, tabelas são resumidas em vez de lidas célula por célula."
        )

    header = lines[0]
    parts = [
        f"Tabela identificada. Cabeçalho principal: {header}.",
        f"Foram detectadas {n_rows} linhas relevantes e aproximadamente {number_count} valores numéricos."
    ]

    terms = []
    for term in ["FV", "GL", "SQ", "QM", "Fc", "p-valor", "tratamentos", "blocos", "total"]:
        if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
            terms.append(term)

    if terms:
        parts.append("Termos principais detectados: " + ", ".join(terms) + ".")

    parts.append("Leitura resumida aplicada para manter clareza na fala.")
    return " ".join(parts)
