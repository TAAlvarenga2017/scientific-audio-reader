from __future__ import annotations

import re

from core.verbalizer_qwen import QwenVerbalizer
from core.document_loader import load_document_text
from core.math import MathDetector, MathEngine


class PipelineResult:
    def __init__(self, prepared_text: str):
        self.prepared_text = prepared_text


class ScientificAudioPipeline:
    def __init__(self):
        self.verbalizer = QwenVerbalizer()
        self.math_detector = MathDetector()
        self.math_engine = MathEngine()

    def _extract_text(self, file_path: str, max_pages: int | None = None) -> str:
        """
        Extrai texto de PDF, DOCX, TXT, MD, HTML, HTM ou TEX.
        """
        return load_document_text(file_path, max_pages=max_pages)

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.replace("￾", "")
        text = text.replace("\ufeff", "")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _mark_missing_math(self, text: str) -> str:
        """
        Marca possíveis expressões matemáticas perdidas na extração.

        Essa função não tenta adivinhar a fórmula.
        Apenas sinaliza que pode haver perda.
        """

        text = re.sub(
            r"=\s*,",
            r"= [expressão matemática não reconhecida],",
            text
        )

        text = re.sub(
            r"se\s*,\s*em que",
            r"se [expressão matemática não reconhecida], em que",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r":\s*\.",
            r": [expressão matemática não reconhecida].",
            text
        )

        return text

    def _split_into_blocks(self, text: str) -> list[dict]:
        """
        Usa o detector genérico de matemática.
        """
        return self.math_detector.split_into_blocks(text)

    def _improve_text_readability(self, text: str) -> str:
        text = text.strip()

        text = re.sub(r"(?m)^(\d+)\s*-\s*", r"Seção \1. ", text)
        text = re.sub(r"(?m)^(\d+\.\d+)\s+", r"Seção \1. ", text)

        text = text.replace("•", " item ")
        text = text.replace("➢", " item ")
        text = text.replace(";", "; ")
        text = text.replace(":", ": ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _verbalize_math(self, content: str) -> str:
        """
        Verbaliza matemática de forma genérica.

        1. Avalia se a extração parece ruim.
        2. Tenta converter para LaTeX.
        3. Converte LaTeX para fala.
        4. Se falhar ou ficar ruim, usa Qwen como fallback.
        """

        result = self.math_engine.process(content)

        spoken = result["speech"]

        # Se a extração matemática parece muito ruim,
        # não devemos fingir que a leitura está correta.
        if result["low_quality"]:
            qwen_spoken = self.verbalizer.verbalize_block({
                "type": "formula",
                "content": content
            })

            if qwen_spoken and not qwen_spoken.startswith("[Erro") and not qwen_spoken.startswith("[Timeout"):
                return qwen_spoken

            return (
                "Expressão matemática possivelmente não reconhecida corretamente "
                "na extração do documento. Conteúdo extraído: "
                + content
            )

        # Se o conversor gerou fala útil, usa.
        if spoken and spoken.strip() and spoken.strip() != content.strip():
            return spoken

        # Fallback com Qwen
        qwen_spoken = self.verbalizer.verbalize_block({
            "type": "formula",
            "content": content
        })

        if qwen_spoken and not qwen_spoken.startswith("[Erro") and not qwen_spoken.startswith("[Timeout"):
            return qwen_spoken

        return spoken or content

    def _verbalize_table(self, content: str) -> str:
        """
        Mantém tabela no Qwen, pois tabela exige sumarização verbal.
        """
        spoken = self.verbalizer.verbalize_block({
            "type": "table",
            "content": content
        })

        if not spoken or spoken.startswith("[Erro") or spoken.startswith("[Timeout"):
            spoken = (
                "Tabela detectada, mas não foi possível verbalizar automaticamente. "
                "Conteúdo extraído: "
                + content
            )

        return spoken

    def prepare(
        self,
        file_path: str,
        max_pages: int | None = None,
        max_blocks: int | None = None,
    ) -> PipelineResult:

        raw_text = self._extract_text(file_path, max_pages=max_pages)
        raw_text = self._normalize_text(raw_text)

        if not raw_text:
            return PipelineResult(prepared_text="")

        # Marca perdas evidentes de matemática, mas sem adivinhar fórmulas.
        raw_text = self._mark_missing_math(raw_text)

        blocks = self._split_into_blocks(raw_text)

        if max_blocks is not None:
            blocks = blocks[:max_blocks]

        spoken_blocks: list[str] = []

        for block in blocks:
            block_type = block["type"]
            content = block["content"].strip()

            if not content:
                continue

            if block_type == "text":
                spoken = self._improve_text_readability(content)

            elif block_type == "math":
                spoken = self._verbalize_math(content)

            elif block_type == "table":
                spoken = self._verbalize_table(content)

            else:
                spoken = content

            if spoken and spoken.strip():
                spoken_blocks.append(spoken.strip())

        final_text = "\n\n".join(spoken_blocks).strip()

        return PipelineResult(prepared_text=final_text)