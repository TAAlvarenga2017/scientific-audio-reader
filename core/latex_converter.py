from __future__ import annotations

import re


class LatexConverter:
    """
    Converte expressões matemáticas simples em uma representação LaTeX.

    Esta primeira versão corrige problemas comuns:
    - ax quando significa a^x;
    - ex quando significa e^x;
    - 2x e 3x em gráficos exponenciais;
    - símbolos gregos;
    - desigualdades;
    - conjuntos reais;
    - frações simples.
    """

    def to_latex(self, expr: str) -> str:
        expr = expr.strip()

        # Normalizações básicas
        expr = expr.replace("IR", r"\mathbb{R}")
        expr = expr.replace("ℝ", r"\mathbb{R}")
        expr = expr.replace("→", r"\to")
        expr = expr.replace("≠", r"\neq")
        expr = expr.replace("≤", r"\leq")
        expr = expr.replace("≥", r"\geq")

        # Algumas vezes a extração transforma ≠ em caractere estranho ou remove.
        expr = expr.replace("=/=", r"\neq")
        expr = expr.replace("!=", r"\neq")

        # Letras gregas
        greek = {
            "α": r"\alpha",
            "β": r"\beta",
            "γ": r"\gamma",
            "δ": r"\delta",
            "ε": r"\varepsilon",
            "θ": r"\theta",
            "λ": r"\lambda",
            "μ": r"\mu",
            "σ": r"\sigma",
            "π": r"\pi",
        }

        for old, new in greek.items():
            expr = expr.replace(old, new)

        # f: R R -> f: R \to R
        # Aqui usamos lambda para evitar erro com \mathbb no re.sub.
        expr = re.sub(
            r"f:\s*\\mathbb\{R\}\s+\\mathbb\{R\}",
            lambda m: r"f: \mathbb{R} \to \mathbb{R}",
            expr
        )

        # f(x) = ax -> f(x) = a^x
        # Regra específica para função exponencial.
        expr = re.sub(
            r"f\(x\)\s*=\s*a\s*x\b",
            lambda m: r"f(x) = a^{x}",
            expr
        )

        # f(x) = ex -> f(x) = e^x
        expr = re.sub(
            r"f\(x\)\s*=\s*e\s*x\b",
            lambda m: r"f(x) = e^{x}",
            expr
        )

        # y = ex, y = 2x, y = 3x -> y = e^x, y = 2^x, y = 3^x
        expr = re.sub(
            r"y\s*=\s*([eE23])\s*x\b",
            lambda m: rf"y = {m.group(1)}^{{x}}",
            expr
        )

        # a^x -> a^{x}
        expr = re.sub(
            r"([a-zA-Z0-9])\^([a-zA-Z0-9]+)",
            lambda m: rf"{m.group(1)}^{{{m.group(2)}}}",
            expr
        )

        # Frações simples: 1/2 -> \frac{1}{2}
        expr = re.sub(
            r"\b(\d+)\s*/\s*(\d+)\b",
            lambda m: rf"\frac{{{m.group(1)}}}{{{m.group(2)}}}",
            expr
        )

        # log_a(b) -> \log_{a}\left(b\right)
        expr = re.sub(
            r"log_([a-zA-Z0-9]+)\(([^)]+)\)",
            lambda m: rf"\log_{{{m.group(1)}}}\left({m.group(2)}\right)",
            expr
        )

        return expr

    def is_probably_latex(self, expr: str) -> bool:
        return "\\" in expr or "^{" in expr or "_{" in expr