from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import gradio as gr

from core.config import OUTPUT_DIR, MAX_CHARS_AUDIO_TEST, MAX_CHARS_PREVIEW_TEXT
from core.pipeline import ScientificAudioPipeline
from tts.audio_utils import safe_filename
from tts.piper_engine import PiperEngine

pipeline = ScientificAudioPipeline()
tts_engine = PiperEngine()


def persist_uploaded_file(pdf_file) -> Path:
    if pdf_file is None:
        raise gr.Error("Envie um arquivo PDF.")

    src = Path(pdf_file)
    if not src.exists():
        raise gr.Error(f"Arquivo temporário não encontrado: {src}")

    temp_dir = Path(tempfile.gettempdir()) / "scientific_audio_reader"
    temp_dir.mkdir(parents=True, exist_ok=True)

    dst = temp_dir / src.name
    shutil.copy2(src, dst)
    return dst


def generate_preview_audio(pdf_file, speed: float, progress=gr.Progress()):
    if pdf_file is None:
        raise gr.Error("Envie um arquivo PDF antes de testar.")

    try:
        progress(0.1, desc="Copiando PDF...")
        stable_pdf = persist_uploaded_file(pdf_file)

        progress(0.35, desc="Interpretando páginas com Qwen2.5-VL...")
        prepared_text = pipeline.prepare(str(stable_pdf)).prepared_text

        progress(0.75, desc="Gerando prévia em áudio...")
        preview_text = prepared_text[:MAX_CHARS_AUDIO_TEST]
        preview_path = OUTPUT_DIR / "preview_audio.wav"
        tts_engine.synthesize(preview_text, preview_path, speed)

        progress(1.0, desc="Prévia pronta.")
        status = (
            f"✅ Prévia pronta.\n"
            f"Velocidade: {speed}\n"
            f"Trecho usado no teste: {len(preview_text)} caracteres"
        )
        return str(preview_path), status

    except Exception as exc:
        raise gr.Error(str(exc)) from exc


def convert_pdf_to_audio(pdf_file, speed: float, progress=gr.Progress()):
    if pdf_file is None:
        raise gr.Error("Envie um arquivo PDF.")

    try:
        progress(0.1, desc="Copiando PDF...")
        stable_pdf = persist_uploaded_file(pdf_file)

        progress(0.35, desc="Interpretando páginas com Qwen2.5-VL...")
        prepared_text = pipeline.prepare(str(stable_pdf)).prepared_text

        progress(0.8, desc="Gerando áudio completo...")
        output_name = safe_filename(Path(stable_pdf).stem) + ".wav"
        output_path = OUTPUT_DIR / output_name
        tts_engine.synthesize(prepared_text, output_path, speed)

        preview = prepared_text[:MAX_CHARS_PREVIEW_TEXT]
        if len(prepared_text) > MAX_CHARS_PREVIEW_TEXT:
            preview += "\n\n[prévia truncada]"

        progress(1.0, desc="Áudio pronto.")
        status = (
            f"✅ Áudio gerado.\n"
            f"Arquivo: {output_name}\n"
            f"Caracteres processados: {len(prepared_text)}"
        )
        return preview, str(output_path), status

    except Exception as exc:
        raise gr.Error(str(exc)) from exc
