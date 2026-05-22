from __future__ import annotations

import re


class MathVerbalizer:
    """
    Verbaliza expressões LaTeX simples para fala em português.
    """

    def latex_to_speech(self, latex: str) -> str:
        text = latex.strip()

        # Remove delimitadores LaTeX
        text = text.replace("$$", "")
        text = text.replace("$", "")

        replacements = {
            r"\mathbb{R}": "conjunto dos números reais",
            r"\beta": "beta",
            r"\alpha": "alfa",
            r"\sigma": "sigma",
            r"\varepsilon": "épsilon",
            r"\epsilon": "épsilon",
            r"\neq": "diferente de",
            r"\leq": "menor ou igual a",
            r"\geq": "maior ou igual a",
            r"\to": "em",
            r"\infty": "infinito",
            "=": " igual a ",
            ">": " maior que ",
            "<": " menor que ",
            "+": " mais ",
            "-": " menos ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # f(x)
        text = re.sub(r"f\(x\)", "f de x", text)

        # a^{x}
        text = re.sub(
            r"([a-zA-Z0-9]+)\s*\^\{([^}]+)\}",
            r"\1 elevado a \2",
            text
        )

        # \frac{1}{2}
        text = re.sub(
            r"\\frac\{([^}]+)\}\{([^}]+)\}",
            r"fração com numerador \1 e denominador \2",
            text
        )

        # \log_{a}\left(b\right)
        text = re.sub(
            r"\\log_\{([^}]+)\}\\left\(([^)]+)\\right\)",
            r"logaritmo de \2 na base \1",
            text
        )

        # Limpeza
        text = re.sub(r"\s+", " ", text).strip()

        return text