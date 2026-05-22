from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup


class MathExtractor:
    """
    Extrai possíveis expressões matemáticas de documentos.

    A ideia é:
    1. Procurar equações nativas do Word em OMML.
    2. Procurar padrões matemáticos em texto.
    3. Marcar expressões que precisam de conversão para LaTeX.
    """

    def extract_omml_from_docx(self, docx_path: str) -> List[str]:
        """
        Extrai blocos OMML de um arquivo .docx.

        OMML é o formato usado pelo Microsoft Word para equações editáveis.
        Esta função ainda não converte para LaTeX; ela apenas localiza as equações.
        """
        docx_path = Path(docx_path)

        if docx_path.suffix.lower() != ".docx":
            return []

        equations = []

        with zipfile.ZipFile(docx_path, "r") as z:
            xml_files = [
                name for name in z.namelist()
                if name.startswith("word/") and name.endswith(".xml")
            ]

            for xml_file in xml_files:
                xml_content = z.read(xml_file).decode("utf-8", errors="ignore")
                soup = BeautifulSoup(xml_content, "xml")

                # Equações em bloco
                for math_block in soup.find_all("m:oMathPara"):
                    equations.append(str(math_block))

                # Equações inline
                for math_inline in soup.find_all("m:oMath"):
                    equations.append(str(math_inline))

        return equations

    def detect_inline_math(self, text: str) -> List[str]:
        """
        Detecta expressões matemáticas simples em texto puro.
        Exemplo: f(x) = ax, a > 0, 0 < a < 1, y = ex etc.
        """
        patterns = [
            r"f\(x\)\s*=\s*[a-zA-Z0-9\^\+\-\*/]+",
            r"[a-zA-Z]\s*[<>]=?\s*[0-9]+",
            r"[0-9]+\s*<\s*[a-zA-Z]\s*<\s*[0-9]+",
            r"log[a-zA-Z0-9_]*\s*\(?[a-zA-Z0-9]+\)?",
            r"[a-zA-Z]\s*=\s*[0-9]+(?:[,.][0-9]+)?",
        ]

        found = []

        for pattern in patterns:
            found.extend(re.findall(pattern, text))

        return found

    def mark_missing_math(self, text: str) -> str:
        """
        Marca lugares onde provavelmente havia fórmula, mas ela foi perdida.
        """
        text = re.sub(
            r"=\s*,",
            r"= [EXPRESSÃO MATEMÁTICA NÃO RECONHECIDA],",
            text
        )

        text = re.sub(
            r"se\s*,\s*em que",
            r"se [EXPRESSÃO MATEMÁTICA NÃO RECONHECIDA], em que",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r":\s*\.",
            r": [EXPRESSÃO MATEMÁTICA NÃO RECONHECIDA].",
            text
        )

        return text