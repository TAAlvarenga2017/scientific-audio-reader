from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile
import os
import unicodedata


class PiperEngine:
    def __init__(self, model_path: str = "voices/pt_BR-voz.onnx"):
        self.model_path = Path(model_path)

    def ensure_ready(self) -> None:
        if not self.model_path.exists():
            raise RuntimeError(f"Modelo de voz não encontrado: {self.model_path}")

        if shutil.which("piper") is None:
            raise RuntimeError(
                "O executável 'piper' não foi encontrado. "
                "Instale o pacote piper-tts e confirme que o comando piper está disponível."
            )

    def _validate_text(self, text: str) -> str:
        if text is None:
            raise RuntimeError("Texto nulo para geração de áudio.")

        clean_text = text.strip()

        if not clean_text:
            raise RuntimeError("Texto vazio para geração de áudio.")

        if len(clean_text) < 10:
            raise RuntimeError("Texto insuficiente para gerar áudio.")

        # bloqueia mensagens de erro do pipeline indo para o TTS
        blocked_prefixes = (
            "[Erro",
            "[Timeout",
            "Erro no modelo",
            "Falha no processamento",
        )

        if clean_text.startswith(blocked_prefixes):
            raise RuntimeError("Falha no processamento do texto antes da geração do áudio.")

        # normaliza acentos, cedilha e outros caracteres Unicode
        clean_text = unicodedata.normalize("NFC", clean_text)

        return clean_text

    def synthesize(self, text: str, output_path: Path | str, speed: float = 1.0) -> None:
        self.ensure_ready()
        clean_text = self._validate_text(text)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if speed <= 0:
            raise RuntimeError("Velocidade inválida. O valor deve ser maior que zero.")

        # Piper usa length_scale: quanto menor, mais rápido
        length_scale = 1.0 / speed

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
            encoding="utf-8"
        ) as temp_input:
            temp_input.write(clean_text)
            temp_input_path = temp_input.name

        try:
            command = [
                "piper",
                "--model", str(self.model_path),
                "--input_file", str(temp_input_path),
                "--output_file", str(output_path),
                "--length_scale", str(length_scale),
            ]

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            if result.returncode != 0:
                stderr_text = result.stderr.decode("utf-8", errors="ignore").strip()
                stdout_text = result.stdout.decode("utf-8", errors="ignore").strip()
                detail = stderr_text or stdout_text or "Erro desconhecido no Piper."
                raise RuntimeError(f"Erro no Piper: {detail}")

            if not output_path.exists():
                raise RuntimeError("O arquivo de áudio não foi criado pelo Piper.")

            # valida se o arquivo não veio vazio/corrompido
            if output_path.stat().st_size < 128:
                raise RuntimeError("O arquivo de áudio gerado é inválido ou está vazio.")

        finally:
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)