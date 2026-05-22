from __future__ import annotations

import re


class LatexConverter:
    """
    Conversor inicial de expressões matemáticas simples para LaTeX.

    Esta versão não resolve toda matemática,
    mas corrige os principais erros do seu protótipo:
    expoentes, letras gregas, logaritmos e frações simples.
    """

    def text_math_to_latex(self, expr: str) -> str:
        expr = expr.strip()

        replacements = {
            "β": r"\beta",
            "α": r"\alpha",
            "σ": r"\sigma",
            "ε": r"\varepsilon",
            "≠": r"\neq",
            "≤": r"\leq",
            "≥": r"\geq",
            "→": r"\to",
            "∞": r"\infty",
            "IR": r"\mathbb{R}",
            "R": r"\mathbb{R}",
        }

        for old, new in replacements.items():
            expr = expr.replace(old, new)

        # Corrige f(x) = ax para f(x) = a^x
        # Cuidado: essa regra é específica para função exponencial.
        expr = re.sub(
            r"f\(x\)\s*=\s*a\s*x\b",
            r"f(x) = a^{x}",
            expr
        )

        # Corrige f(x) = ex para f(x) = e^x
        expr = re.sub(
            r"f\(x\)\s*=\s*e\s*x\b",
            r"f(x) = e^{x}",
            expr
        )

        # Transforma a^x em a^{x}
        expr = re.sub(
            r"([a-zA-Z])\^([a-zA-Z0-9]+)",
            r"\1^{\2}",
            expr
        )

        # Transforma 2x, 3x, ex em 2^x, 3^x, e^x quando estiver em contexto de y =
        expr = re.sub(
            r"y\s*=\s*([23e])x\b",
            r"y = \1^{x}",
            expr
        )

        # Frações simples: 1/2 -> \frac{1}{2}
        expr = re.sub(
            r"\b(\d+)\s*/\s*(\d+)\b",
            r"\\frac{\1}{\2}",
            expr
        )

        # log_a b escrito como log_a(b)
        expr = re.sub(
            r"log_([a-zA-Z0-9]+)\(([^)]+)\)",
            r"\\log_{\1}\left(\2\right)",
            expr
        )

        return expr

    def wrap_latex(self, expr: str, inline: bool = True) -> str:
        latex = self.text_math_to_latex(expr)

        if inline:
            return f"${latex}$"

        return f"$$\n{latex}\n$$"