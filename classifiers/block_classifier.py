from __future__ import annotations
from core.types import DocumentBlock
from classifiers.heuristics import classify_block_type

class BlockClassifier:
    def classify(self, blocks: list[DocumentBlock]) -> list[DocumentBlock]:
        for block in blocks:
            block.block_type, block.score = classify_block_type(block.raw_text)
        return blocks
