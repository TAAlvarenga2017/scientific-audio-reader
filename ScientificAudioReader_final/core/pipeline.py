from __future__ import annotations

from core.pdf_pages import pdf_to_images
from core.parser_llava import QwenVLParser
from core.verbalizer_qwen import QwenVerbalizer


class PipelineResult:
    def __init__(self, prepared_text: str):
        self.prepared_text = prepared_text


class ScientificAudioPipeline:
    """
    Pipeline final:
    PDF/página -> Qwen2.5-VL -> blocos estruturados -> Qwen2.5 verbalizador fiel -> TTS
    """
    def __init__(self):
        self.parser = QwenVLParser()
        self.verbalizer = QwenVerbalizer()

    def prepare(self, pdf_path: str, mode: str | None = None) -> PipelineResult:
        page_images = pdf_to_images(pdf_path)
        spoken_blocks: list[str] = []

        for image_path in page_images:
            blocks = self.parser.parse_page_image(image_path)
            for block in blocks:
                spoken = self.verbalizer.verbalize_block(block)
                if spoken:
                    spoken_blocks.append(spoken)

        prepared_text = "\n\n".join(spoken_blocks).strip()
        return PipelineResult(prepared_text=prepared_text)
