from __future__ import annotations

from .latex_converter import LatexConverter
from .latex_speaker import LatexSpeaker
from .math_quality import MathQuality


class MathEngine:
    """
    Motor genérico de matemática.

    Fluxo:
    matemática textual
       ↓
    tentativa de LaTeX
       ↓
    fala matemática
       ↓
    avaliação de qualidade
    """

    def __init__(self):
        self.converter = LatexConverter()
        self.speaker = LatexSpeaker()
        self.quality = MathQuality()

    def to_latex(self, content: str) -> str:
        return self.converter.to_latex(content)

    def to_speech(self, content: str) -> str:
        latex = self.to_latex(content)
        speech = self.speaker.speak(latex)
        return speech

    def is_low_quality(self, content: str) -> bool:
        return self.quality.is_bad(content)

    def process(self, content: str) -> dict:
        """
        Retorna informações úteis para debug e avaliação científica.
        """
        latex = self.to_latex(content)
        speech = self.speaker.speak(latex)
        quality_score = self.quality.score(content)

        return {
            "original": content,
            "latex": latex,
            "speech": speech,
            "quality_score": quality_score,
            "low_quality": self.quality.is_bad(content),
        }