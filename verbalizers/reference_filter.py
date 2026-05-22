from __future__ import annotations

def should_skip_reference(text: str, mode: str) -> bool:
    return mode != "Acadêmico"
