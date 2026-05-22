from __future__ import annotations

import re


class MathDetector:
    """
    Detecta blocos matemáticos de forma genérica.

    A ideia não é reconhecer uma fórmula específica,
    mas identificar padrões comuns em matemática, estatística
    e ciências exatas.
    """

    def is_math_line(self, line: str) -> bool:
        line = line.strip()

        if not line:
            return False

        math_symbols = (
            r"[=+\-*/^_(){}\[\]<>]"
            r"|[√∑∏∫∞≈≠≤≥±×÷→←↔]"
            r"|[αβγδεζηθικλμνξοπρστυφχψω]"
            r"|[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]"
            r"|[𝛼𝛽𝛾𝛿𝜀𝜃𝜆𝜇𝜎𝜋]"
        )

        if re.search(math_symbols, line):
            return True

        math_words = [
            r"\blog\b",
            r"\bln\b",
            r"\bsen\b",
            r"\bcos\b",
            r"\btan\b",
            r"\blim\b",
            r"\bmax\b",
            r"\bmin\b",
            r"\bvar\b",
            r"\bE\s*\(",
            r"\bP\s*\(",
            r"\bPr\s*\(",
            r"\bCov\s*\(",
            r"\bCorr\s*\(",
            r"\bp-?valor\b",
            r"\bp-value\b",
            r"\bR\^?2\b",
            r"\bR²\b",
        ]

        if any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in math_words):
            return True

        # Expressões com variáveis e números
        patterns = [
            r"[a-zA-Z]\s*=\s*[-+]?\d",
            r"[a-zA-Z]\s*[<>]=?\s*[-+]?\d",
            r"\d+\s*[<>]=?\s*[a-zA-Z]",
            r"[a-zA-Z]\([a-zA-Z0-9]\)",
            r"[a-zA-Z]\s*\^\s*[0-9a-zA-Z]",
            r"[a-zA-Z]\s*_\s*[0-9a-zA-Z]",
        ]

        return any(re.search(pattern, line) for pattern in patterns)

    def looks_like_table_line(self, line: str) -> bool:
        line = line.strip()

        if not line:
            return False

        if "|" in line or "\t" in line:
            return True

        numbers = re.findall(r"\d+[.,]?\d*", line)

        # Muitas colunas numéricas indicam tabela.
        if len(numbers) >= 5:
            return True

        # Sequência com separadores repetidos
        if len(re.findall(r"\s{2,}", line)) >= 3:
            return True

        return False

    def split_into_blocks(self, text: str) -> list[dict]:
        """
        Separa o documento em blocos:
        - text
        - math
        - table
        """
        lines = text.split("\n")

        blocks: list[dict] = []
        buffer_text: list[str] = []
        buffer_math: list[str] = []
        buffer_table: list[str] = []

        def flush_text():
            nonlocal buffer_text
            if buffer_text:
                content = " ".join(x.strip() for x in buffer_text if x.strip())
                if content:
                    blocks.append({"type": "text", "content": content})
                buffer_text = []

        def flush_math():
            nonlocal buffer_math
            if buffer_math:
                content = "\n".join(x.strip() for x in buffer_math if x.strip())
                if content:
                    blocks.append({"type": "math", "content": content})
                buffer_math = []

        def flush_table():
            nonlocal buffer_table
            if buffer_table:
                content = "\n".join(x.strip() for x in buffer_table if x.strip())
                if content:
                    blocks.append({"type": "table", "content": content})
                buffer_table = []

        for line in lines:
            clean = line.strip()

            if not clean:
                flush_text()
                flush_math()
                flush_table()
                continue

            is_table = self.looks_like_table_line(clean)
            is_math = self.is_math_line(clean)

            if is_table and not is_math:
                flush_text()
                flush_math()
                buffer_table.append(clean)

            elif is_math:
                flush_text()
                flush_table()
                buffer_math.append(clean)

            else:
                flush_math()
                flush_table()
                buffer_text.append(clean)

        flush_text()
        flush_math()
        flush_table()

        return blocks