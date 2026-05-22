from __future__ import annotations
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from core.config import VOICE_MODEL, VOICE_CONFIG

class PiperEngine:
    def ensure_ready(self) -> None:
        if shutil.which("piper") is None:
            raise RuntimeError(
                "O executável 'piper' não foi encontrado. Instale o pacote piper-tts e confirme que o comando piper está disponível."
            )
        if not VOICE_MODEL.exists():
            raise FileNotFoundError(f"Modelo de voz não encontrado: {VOICE_MODEL}")
        if not VOICE_CONFIG.exists():
            raise FileNotFoundError(f"Arquivo de configuração da voz não encontrado: {VOICE_CONFIG}")

    def synthesize(self, text: str, output_path: Path, speed: float) -> None:
        self.ensure_ready()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(text)
            temp_txt = temp_file.name

        try:
            command = [
                "piper",
                "--model", str(VOICE_MODEL),
                "--config", str(VOICE_CONFIG),
                "--input-file", temp_txt,
                "--output-file", str(output_path),
                "--length-scale", str(speed),
            ]

            result = subprocess.run(command, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                error_msg = result.stderr.strip() or result.stdout.strip() or "Erro desconhecido ao executar o Piper."
                raise RuntimeError(error_msg)

            if not output_path.exists():
                raise RuntimeError("O arquivo de áudio não foi criado.")
        finally:
            if os.path.exists(temp_txt):
                os.remove(temp_txt)
