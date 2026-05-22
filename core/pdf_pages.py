from __future__ import annotations

from pathlib import Path
import tempfile
import pymupdf

def pdf_to_images(pdf_path: str, dpi: int = 110) -> list[str]:
    doc = pymupdf.open(pdf_path)
    temp_dir = Path(tempfile.gettempdir()) / "scientific_audio_reader_pages"
    temp_dir.mkdir(parents=True, exist_ok=True)

    images: list[str] = []
    scale = dpi / 72.0
    matrix = pymupdf.Matrix(scale, scale)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = temp_dir / f"page_{i+1:03d}.jpg"
        pix.save(str(out), jpg_quality=70)
        images.append(str(out))

    doc.close()
    return images