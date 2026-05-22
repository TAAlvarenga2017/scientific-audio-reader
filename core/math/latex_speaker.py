from __future__ import annotations

import re


class LatexSpeaker:
    """
    Converte LaTeX simples para fala em português.

    Objetivo: transformar matemática em texto pronunciável pelo TTS.
    """

    def speak(self, latex: str) -> str:
        text = latex.strip()

        if not text:
            return ""

        text = self._remove_delimiters(text)
        text = self._speak_fractions(text)
        text = self._speak_roots(text)
        text = self._speak_sums_integrals_limits(text)
        text = self._speak_powers(text)
        text = self._speak_indices(text)
        text = self._speak_functions(text)
        text = self._replace_symbols(text)
        text = self._cleanup(text)

        return text

    def _remove_delimiters(self, text: str) -> str:
        text = text.replace("$$", "")
        text = text.replace("$", "")
        text = text.replace(r"\[", "")
        text = text.replace(r"\]", "")
        text = text.replace(r"\(", "")
        text = text.replace(r"\)", "")
        return text

    def _speak_fractions(self, text: str) -> str:
        # \frac{a}{b}
        pattern = r"\\frac\{([^{}]+)\}\{([^{}]+)\}"

        while re.search(pattern, text):
            text = re.sub(
                pattern,
                lambda m: f"fração com numerador {m.group(1)} e denominador {m.group(2)}",
                text
            )

        return text

    def _speak_roots(self, text: str) -> str:
        # \sqrt{x}
        text = re.sub(
            r"\\sqrt\{([^{}]+)\}",
            lambda m: f"raiz quadrada de {m.group(1)}",
            text
        )

        return text

    def _speak_sums_integrals_limits(self, text: str) -> str:
        text = text.replace(r"\sum", " somatório ")
        text = text.replace(r"\prod", " produtório ")
        text = text.replace(r"\int", " integral ")
        text = text.replace(r"\lim", " limite ")
        return text

    def _speak_powers(self, text: str) -> str:
        # x^{2}
        text = re.sub(
            r"([a-zA-Z0-9\\]+)\^\{2\}",
            lambda m: f"{m.group(1)} ao quadrado",
            text
        )

        # x^{3}
        text = re.sub(
            r"([a-zA-Z0-9\\]+)\^\{3\}",
            lambda m: f"{m.group(1)} ao cubo",
            text
        )

        # x^{n}
        text = re.sub(
            r"([a-zA-Z0-9\\]+)\^\{([^{}]+)\}",
            lambda m: f"{m.group(1)} elevado a {m.group(2)}",
            text
        )

        return text

    def _speak_indices(self, text: str) -> str:
        # beta_{0}
        text = re.sub(
            r"([a-zA-Z0-9\\]+)_\{([^{}]+)\}",
            lambda m: f"{m.group(1)} índice {m.group(2)}",
            text
        )

        return text

    def _speak_functions(self, text: str) -> str:
        replacements = {
            r"\log": " logaritmo ",
            r"\ln": " logaritmo natural ",
            r"\sin": " seno ",
            r"\cos": " cosseno ",
            r"\tan": " tangente ",
            r"\max": " máximo ",
            r"\min": " mínimo ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _replace_symbols(self, text: str) -> str:
        replacements = {
            r"\mathbb{R}": "conjunto dos números reais",
            r"\mathbb{N}": "conjunto dos números naturais",
            r"\mathbb{Z}": "conjunto dos números inteiros",
            r"\mathbb{Q}": "conjunto dos números racionais",
            r"\mathbb{C}": "conjunto dos números complexos",

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
            r"\Delta": "delta",
            r"\Sigma": "sigma maiúsculo",
            r"\Pi": "pi maiúsculo",
            r"\Omega": "ômega",

            r"\neq": " diferente de ",
            r"\leq": " menor ou igual a ",
            r"\geq": " maior ou igual a ",
            r"\approx": " aproximadamente igual a ",
            r"\pm": " mais ou menos ",
            r"\times": " vezes ",
            r"\div": " dividido por ",
            r"\cdot": " vezes ",
            r"\to": " em ",
            r"\leftarrow": " vem de ",
            r"\leftrightarrow": " se e somente se ",
            r"\infty": " infinito ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        simple = {
            "=": " igual a ",
            ">": " maior que ",
            "<": " menor que ",
            "+": " mais ",
            "-": " menos ",
            "*": " vezes ",
            "/": " dividido por ",
            "(": " abre parênteses ",
            ")": " fecha parênteses ",
            "[": " abre colchetes ",
            "]": " fecha colchetes ",
            "{": " abre chaves ",
            "}": " fecha chaves ",
        }

        for old, new in simple.items():
            text = text.replace(old, new)

        return text

    def _cleanup(self, text: str) -> str:
        # Remove comandos LaTeX que sobraram
        text = text.replace("\\", " ")

        # Ajustes de leitura
        text = text.replace("f abre parênteses x fecha parênteses", "f de x")
        text = text.replace("g abre parênteses x fecha parênteses", "g de x")
        text = text.replace("P abre parênteses", "probabilidade de ")
        text = text.replace("E abre parênteses", "esperança de ")

        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        return text