from __future__ import annotations
from core.types import DocumentBlock

def split_page_into_blocks(page_text: str, page_number: int) -> list[DocumentBlock]:
    chunks = [chunk.strip() for chunk in page_text.split("\n\n") if chunk.strip()]
    return [DocumentBlock(page_number=page_number, raw_text=chunk) for chunk in chunks]
