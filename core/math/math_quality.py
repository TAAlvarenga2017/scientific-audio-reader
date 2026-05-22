from __future__ import annotations

import re


class MathQuality:
    """
    Avalia a qualidade de um bloco matemático extraído.

    Não tenta corrigir fórmula específica.
    Apenas identifica sinais de que a extração ficou ruim.
    """

    def score(self, text: str) -> int:
        """
        Quanto maior o score, maior a chance de erro na extração.
        """
        text = text.strip()
        score = 0

        if not text:
            return 10

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Muitas linhas com um único símbolo indicam fórmula quebrada.
        one_token_lines = 0
        for line in lines:
            if len(line.split()) <= 1 and len(line) <= 4:
                one_token_lines += 1

        if one_token_lines >= 2:
            score += 2

        # Sinal de igualdade sem termos suficientes.
        if "=" in text and len(re.findall(r"[a-zA-Z0-9]", text)) < 3:
            score += 2

        # Termina em operador.
        if re.search(r"[+\-*/=]\s*$", text):
            score += 2

        # Começa com operador.
        if re.search(r"^\s*[+\-*/=]", text):
            score += 1

        # Muitos operadores e poucas variáveis/números.
        operators = len(re.findall(r"[+\-*/=<>]", text))
        operands = len(re.findall(r"[a-zA-Z0-9]", text))

        if operators >= 3 and operands <= 3:
            score += 2

        # Muitos saltos de linha em fórmula curta.
        if len(lines) >= 4 and len(text) < 80:
            score += 2

        # Marcador explícito de falha.
        if "não reconhecida" in text.lower():
            score += 3

        return score

    def is_bad(self, text: str, threshold: int = 4) -> bool:
        return self.score(text) >= threshold