from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import gradio as gr

from core.pipeline import ScientificAudioPipeline
from core.config import OUTPUT_DIR, MAX_CHARS_AUDIO_TEST, MAX_CHARS_PREVIEW_TEXT
from tts.piper_engine import PiperEngine
from tts.audio_utils import safe_filename


pipeline = ScientificAudioPipeline()
tts_engine = PiperEngine()

# garante pasta de saída
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".html",
    ".htm",
    ".tex",
}


# =========================================================
# 📂 Garante que o documento não seja perdido (Gradio temp fix)
# =========================================================
def persist_uploaded_file(uploaded_file) -> Path:
    if uploaded_file is None:
        raise gr.Error("Envie um documento.")

    src = Path(uploaded_file)

    if not src.exists():
        raise gr.Error(f"Arquivo temporário não encontrado: {src}")

    suffix = src.suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise gr.Error(
            "Arquivo inválido. Envie PDF, DOCX, TXT, MD, HTML ou TEX."
        )

    temp_dir = Path(tempfile.gettempdir()) / "scientific_audio_reader"
    temp_dir.mkdir(parents=True, exist_ok=True)

    dst = temp_dir / src.name
    shutil.copy2(src, dst)
    return dst


# =========================================================
# 🔊 PRÉVIA RÁPIDA
# =========================================================
def generate_preview_audio(uploaded_file, speed: float, progress=gr.Progress()):
    if uploaded_file is None:
        raise gr.Error("Envie um documento antes de testar.")

    if speed is None or speed <= 0:
        raise gr.Error("Velocidade inválida.")

    try:
        progress(0.1, desc="Preparando documento...")
        stable_file = persist_uploaded_file(uploaded_file)

        # processa só o começo do documento
        progress(0.35, desc="Lendo início do conteúdo...")
        prepared_text = pipeline.prepare(
            str(stable_file),
            max_pages=2,
            max_blocks=6
        ).prepared_text

        # validação mínima
        if not prepared_text or len(prepared_text.strip()) < 5:
            raise gr.Error("Não foi possível extrair conteúdo suficiente do documento.")

        progress(0.75, desc="Gerando prévia em áudio...")
        preview_text = prepared_text[:MAX_CHARS_AUDIO_TEST].strip()

        if len(preview_text) < 5:
            raise gr.Error("A prévia gerada ficou muito curta.")

        preview_path = OUTPUT_DIR / "preview_audio.wav"
        tts_engine.synthesize(preview_text, preview_path, speed)

        progress(1.0, desc="Prévia pronta.")

        status = (
            f"✅ Prévia pronta\n"
            f"Arquivo: {stable_file.name}\n"
            f"Formato: {stable_file.suffix.lower()}\n"
            f"Velocidade: {speed}\n"
            f"Caracteres usados: {len(preview_text)}"
        )

        return str(preview_path), status

    except Exception as exc:
        raise gr.Error(str(exc)) from exc


# =========================================================
# 🎧 ÁUDIO COMPLETO
# =========================================================
def convert_pdf_to_audio(uploaded_file, speed: float, progress=gr.Progress()):
    if uploaded_file is None:
        raise gr.Error("Envie um documento.")

    if speed is None or speed <= 0:
        raise gr.Error("Velocidade inválida.")

    try:
        progress(0.1, desc="Preparando documento...")
        stable_file = persist_uploaded_file(uploaded_file)

        progress(0.35, desc="Processando conteúdo do documento...")
        prepared_text = pipeline.prepare(str(stable_file)).prepared_text

        if not prepared_text or len(prepared_text.strip()) < 50:
            raise gr.Error("Conteúdo insuficiente para gerar áudio.")

        progress(0.8, desc="Gerando áudio completo...")

        output_name = safe_filename(stable_file.stem) + ".wav"
        output_path = OUTPUT_DIR / output_name

        tts_engine.synthesize(prepared_text, output_path, speed)

        preview = prepared_text[:MAX_CHARS_PREVIEW_TEXT]
        if len(prepared_text) > MAX_CHARS_PREVIEW_TEXT:
            preview += "\n\n[prévia truncada]"

        progress(1.0, desc="Áudio pronto.")

        status = (
            f"✅ Áudio gerado com sucesso\n"
            f"Arquivo original: {stable_file.name}\n"
            f"Formato: {stable_file.suffix.lower()}\n"
            f"Áudio gerado: {output_name}\n"
            f"Caracteres processados: {len(prepared_text)}"
        )

        return preview, str(output_path), status

    except Exception as exc:
        raise gr.Error(str(exc)) from exc