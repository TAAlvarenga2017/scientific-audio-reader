from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional

BlockType = Literal["title", "text", "equation", "table", "reference", "unknown"]

@dataclass
class DocumentBlock:
    page_number: int
    raw_text: str
    block_type: BlockType = "unknown"
    verbalized_text: str = ""
    score: float = 0.0
    metadata: dict = field(default_factory=dict)

@dataclass
class PipelineResult:
    original_text: str
    prepared_text: str
    blocks: list[DocumentBlock]
    output_path: Optional[str] = None
    info: Optional[str] = None
