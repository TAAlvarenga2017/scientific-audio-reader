from __future__ import annotations
import unicodedata

import re


class LatexConverter:
    """
    Conversor genérico de matemática textual para LaTeX.

    Não depende do tema.
    Atua sobre estruturas:
    - expoentes
    - índices
    - frações simples
    - raízes
    - letras gregas
    - operadores
    - notação estatística comum
    """

    def to_latex(self, expr: str) -> str:
        expr = expr.strip()

        if not expr:
            return ""

        expr = unicodedata.normalize("NFKC", expr)

        return expr.strip()

    def _normalize_unicode(self, expr: str) -> str:
        replacements = {
            "−": "-",
            "–": "-",
            "—": "-",
            "×": r"\times",
            "÷": r"\div",
            "·": r"\cdot",
            "√": r"\sqrt",
            "∞": r"\infty",
            "≈": r"\approx",
            "≠": r"\neq",
            "≤": r"\leq",
            "≥": r"\geq",
            "±": r"\pm",
            "→": r"\to",
            "←": r"\leftarrow",
            "↔": r"\leftrightarrow",
        }

        for old, new in replacements.items():
            expr = expr.replace(old, new)

        return expr

    def _replace_greek(self, expr: str) -> str:
        greek = {
            "α": r"\alpha",
            "β": r"\beta",
            "γ": r"\gamma",
            "δ": r"\delta",
            "ε": r"\varepsilon",
            "ζ": r"\zeta",
            "η": r"\eta",
            "θ": r"\theta",
            "ι": r"\iota",
            "κ": r"\kappa",
            "λ": r"\lambda",
            "μ": r"\mu",
            "ν": r"\nu",
            "ξ": r"\xi",
            "π": r"\pi",
            "ρ": r"\rho",
            "σ": r"\sigma",
            "τ": r"\tau",
            "φ": r"\phi",
            "χ": r"\chi",
            "ψ": r"\psi",
            "ω": r"\omega",
            "Δ": r"\Delta",
            "Σ": r"\Sigma",
            "Π": r"\Pi",
            "Ω": r"\Omega",
        }

        for old, new in greek.items():
            expr = expr.replace(old, new)

        return expr

    def _replace_sets(self, expr: str) -> str:
        replacements = {
            "ℝ": r"\mathbb{R}",
            "ℕ": r"\mathbb{N}",
            "ℤ": r"\mathbb{Z}",
            "ℚ": r"\mathbb{Q}",
            "ℂ": r"\mathbb{C}",
            "IR": r"\mathbb{R}",
        }

        for old, new in replacements.items():
            expr = expr.replace(old, new)

        return expr

    def _replace_operators(self, expr: str) -> str:
        expr = expr.replace("=/=", r"\neq")
        expr = expr.replace("!=", r"\neq")
        expr = expr.replace(">=", r"\geq")
        expr = expr.replace("<=", r"\leq")
        return expr

    def _convert_superscripts(self, expr: str) -> str:
        superscripts = {
            "⁰": "0",
            "¹": "1",
            "²": "2",
            "³": "3",
            "⁴": "4",
            "⁵": "5",
            "⁶": "6",
            "⁷": "7",
            "⁸": "8",
            "⁹": "9",
            "ⁿ": "n",
        }

        # x² -> x^{2}
        pattern = r"([a-zA-Z0-9\)])([" + "".join(superscripts.keys()) + r"]+)"

        def repl(match):
            base = match.group(1)
            sup = "".join(superscripts.get(ch, ch) for ch in match.group(2))
            return rf"{base}^{{{sup}}}"

        return re.sub(pattern, repl, expr)

    def _convert_subscripts(self, expr: str) -> str:
        subscripts = {
            "₀": "0",
            "₁": "1",
            "₂": "2",
            "₃": "3",
            "₄": "4",
            "₅": "5",
            "₆": "6",
            "₇": "7",
            "₈": "8",
            "₉": "9",
        }

        pattern = r"([a-zA-Z0-9\)])([" + "".join(subscripts.keys()) + r"]+)"

        def repl(match):
            base = match.group(1)
            sub = "".join(subscripts.get(ch, ch) for ch in match.group(2))
            return rf"{base}_{{{sub}}}"

        return re.sub(pattern, repl, expr)

    def _convert_caret_exponents(self, expr: str) -> str:
        # x^2 -> x^{2}
        expr = re.sub(
            r"([a-zA-Z0-9\)])\^([a-zA-Z0-9]+)",
            lambda m: rf"{m.group(1)}^{{{m.group(2)}}}",
            expr
        )

        return expr

    def _convert_underscore_indices(self, expr: str) -> str:
        # beta_0 -> beta_{0}
        expr = re.sub(
            r"([a-zA-Z0-9\\]+)_([a-zA-Z0-9]+)",
            lambda m: rf"{m.group(1)}_{{{m.group(2)}}}",
            expr
        )

        return expr

    def _convert_simple_fractions(self, expr: str) -> str:
        # 1/2 -> \frac{1}{2}
        expr = re.sub(
            r"\b(\d+)\s*/\s*(\d+)\b",
            lambda m: rf"\frac{{{m.group(1)}}}{{{m.group(2)}}}",
            expr
        )

        # a/b -> \frac{a}{b}, apenas quando isolado
        expr = re.sub(
            r"\b([a-zA-Z])\s*/\s*([a-zA-Z])\b",
            lambda m: rf"\frac{{{m.group(1)}}}{{{m.group(2)}}}",
            expr
        )

        return expr

    def _convert_roots(self, expr: str) -> str:
        # sqrt(x) -> \sqrt{x}
        expr = re.sub(
            r"sqrt\s*\(([^)]+)\)",
            lambda m: rf"\sqrt{{{m.group(1)}}}",
            expr,
            flags=re.IGNORECASE
        )

        # \sqrt x -> \sqrt{x}
        expr = re.sub(
            r"\\sqrt\s+([a-zA-Z0-9\\]+)",
            lambda m: rf"\sqrt{{{m.group(1)}}}",
            expr
        )

        return expr

    def _convert_functions(self, expr: str) -> str:
        functions = [
            "log",
            "ln",
            "sin",
            "cos",
            "tan",
            "sen",
            "lim",
            "max",
            "min",
        ]

        for func in functions:
            expr = re.sub(
                rf"\b{func}\b",
                rf"\\{func}",
                expr,
                flags=re.IGNORECASE
            )

        # Em português, sen(x) é seno.
        expr = expr.replace(r"\sen", r"\sin")

        return expr

    def is_latex_like(self, expr: str) -> bool:
        return "\\" in expr or "^{" in expr or "_{" in expr or r"\frac" in expr