from __future__ import annotations
import pymupdf
from core.types import DocumentBlock
from parsers.block_extractor import split_page_into_blocks

class PDFParser:
    def parse(self, pdf_path: str) -> list[DocumentBlock]:
        blocks: list[DocumentBlock] = []
        with pymupdf.open(pdf_path) as doc:
            for page_index, page in enumerate(doc):
                text = page.get_text("text", sort=True)
                if text and text.strip():
                    blocks.extend(split_page_into_blocks(text.strip(), page_index + 1))

        if not blocks:
            raise ValueError(
                "Não foi possível extrair texto do PDF. O arquivo pode ser escaneado ou conter apenas imagens."
            )
        return blocks
