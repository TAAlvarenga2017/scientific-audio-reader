from __future__ import annotations

import re


class LatexSpeaker:
    """
    Transforma LaTeX simples em texto falado em português.
    """

    def speak(self, latex: str) -> str:
        text = latex.strip()

        # Remove delimitadores caso existam
        text = text.replace("$$", "")
        text = text.replace("$", "")

        # Frações primeiro
        text = re.sub(
            r"\\frac\{([^}]+)\}\{([^}]+)\}",
            r"fração com numerador \1 e denominador \2",
            text
        )

        # Expoentes: a^{x}
        text = re.sub(
            r"([a-zA-Z0-9]+)\^\{([^}]+)\}",
            r"\1 elevado a \2",
            text
        )

        # Índices: beta_{0}
        text = re.sub(
            r"([a-zA-Z\\]+)_\{([^}]+)\}",
            r"\1 índice \2",
            text
        )

        # Logaritmo
        text = re.sub(
            r"\\log_\{([^}]+)\}\\left\(([^)]+)\\right\)",
            r"logaritmo de \2 na base \1",
            text
        )

        replacements = {
            r"\mathbb{R}": "conjunto dos números reais",
            r"\to": "em",
            r"\neq": "diferente de",
            r"\leq": "menor ou igual a",
            r"\geq": "maior ou igual a",
            r"\alpha": "alfa",
            r"\beta": "beta",
            r"\gamma": "gama",
            r"\delta": "delta",
            r"\varepsilon": "épsilon",
            r"\epsilon": "épsilon",
            r"\theta": "teta",
            r"\lambda": "lambda",
            r"\mu": "mi",
            r"\sigma": "sigma",
            r"\pi": "pi",
            "=": " igual a ",
            ">": " maior que ",
            "<": " menor que ",
            "+": " mais ",
            "-": " menos ",
            "*": " vezes ",
            "/": " dividido por ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = text.replace("f(x)", "f de x")
        text = text.replace("g(x)", "g de x")

        # Limpeza final
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        return text