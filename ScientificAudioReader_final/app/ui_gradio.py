from __future__ import annotations

import gradio as gr
from core.config import DEFAULT_SPEED
from app.controller import convert_pdf_to_audio, generate_preview_audio

theme = gr.themes.Base().set(
    body_background_fill="#111827",
    body_background_fill_dark="#111827",
    background_fill_primary="#111827",
    background_fill_primary_dark="#111827",
    background_fill_secondary="#0f172a",
    background_fill_secondary_dark="#0f172a",
    block_background_fill="#0f172a",
    block_background_fill_dark="#0f172a",
    block_border_color="rgba(255,255,255,0.08)",
    block_border_color_dark="rgba(255,255,255,0.08)",
    input_background_fill="#0f172a",
    input_background_fill_dark="#0f172a",
    input_border_color="rgba(255,255,255,0.08)",
    input_border_color_dark="rgba(255,255,255,0.08)",
    button_primary_background_fill="#132a5c",
    button_primary_background_fill_hover="#1d4ed8",
    button_primary_text_color="white",
    button_secondary_background_fill="#0f172a",
    button_secondary_background_fill_hover="#111827",
    button_secondary_text_color="#f8fafc",
    color_accent="#3b82f6",
    color_accent_soft="#1e3a8a",
    body_text_color="#f8fafc",
    body_text_color_subdued="#94a3b8",
    border_color_primary="rgba(255,255,255,0.08)",
    border_color_accent="#3b82f6",
)

CUSTOM_CSS = """
html, body, #root {
  background: #111827 !important;
  margin: 0;
  padding: 0;
}

body {
  background: linear-gradient(135deg, #0b1120, #111827 60%, #1f2937 100%) !important;
}

.gradio-container {
  max-width: 1440px !important;
  margin: 0 auto !important;
  padding: 20px 28px 32px 28px !important;
  background: transparent !important;
}

.block-container,
.gradio-container .block-container,
.gradio-container .gr-box,
.gradio-container .gr-form,
.gradio-container .gr-group,
.gradio-container .gr-panel,
.main,
.app {
  background: transparent !important;
  border-color: transparent !important;
}

.hero-card {
  background: linear-gradient(135deg, #111827, #0f172a);
  border-radius: 22px;
  padding: 28px;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 20px 50px rgba(0,0,0,0.45);
}

.section-card {
  background: rgba(17, 24, 39, 0.96);
  border-radius: 18px;
  padding: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 24px rgba(0,0,0,0.20);
}

.side-card {
  background: rgba(15, 23, 42, 0.96);
  border-radius: 18px;
  padding: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.info-card {
  background: rgba(30, 41, 59, 0.72);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  padding: 14px 16px;
}

.info-card:empty {
  display: none !important;
}

h1, h2, h3, h4, p, li {
  color: #f8fafc !important;
}

.helper-text {
  color: #94a3b8 !important;
  font-size: 0.95rem;
  line-height: 1.55;
}

.muted-text {
  color: #cbd5e1 !important;
  font-size: 0.92rem;
  line-height: 1.5;
}

.gradio-container .gr-input,
.gradio-container .gr-file,
.gradio-container .gr-slider,
textarea,
input,
select {
  background: #0f172a !important;
  color: #f8fafc !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important;
}

.gradio-container .gr-file > div {
  background: #0f172a !important;
  border: 1px dashed rgba(255,255,255,0.15) !important;
}

textarea::placeholder,
input::placeholder {
  color: #64748b !important;
}

button {
  border-radius: 14px !important;
  font-weight: 600 !important;
  min-height: 46px !important;
}

button.primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
  color: white !important;
  border: none !important;
}

button.secondary {
  background: #0f172a !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: #f8fafc !important;
}

.soft-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
  margin: 14px 0;
}

.footer-note {
  color: #94a3b8;
  text-align: center;
  font-size: 0.9rem;
  margin-top: 12px;
}

.tag {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(59,130,246,0.14);
  color: #93c5fd;
  font-size: 0.82rem;
  font-weight: 600;
  border: 1px solid rgba(59,130,246,0.18);
  margin-bottom: 8px;
}
"""

with gr.Blocks(
    title="Scientific Audio Reader",
    theme=theme,
    css=CUSTOM_CSS,
) as demo:

    gr.Markdown(
        """
        <div class="hero-card">
            <div class="tag">Qwen local + Ollama</div>
            <h1 style="margin-top: 4px; margin-bottom: 8px;">🎧 Scientific Audio Reader</h1>
            <p class="helper-text" style="font-size:1rem; margin:0;">
                Leitura inteligente de documentos científicos em áudio, com verbalização fiel de fórmulas.
            </p>
        </div>
        """
    )

    gr.Markdown('<div class="soft-divider"></div>')

    with gr.Row(equal_height=True):
        with gr.Column(scale=3, min_width=280):
            gr.Markdown(
                """
                <div class="side-card">
                    <h3 style="margin-top:0;">📘 Como funciona</h3>

                    <p class="helper-text">
                        O aplicativo interpreta páginas do PDF com Qwen2.5-VL, transforma o conteúdo
                        em leitura oral fiel e gera o áudio localmente.
                    </p>

                    <div class="info-card" style="margin-top:12px;">
                        <h4 style="margin-top:0; margin-bottom:8px;">Etapas</h4>
                        <p class="muted-text" style="margin:0;">
                            1. Envie o PDF<br>
                            2. Ajuste a velocidade<br>
                            3. Teste a prévia<br>
                            4. Gere o áudio final
                        </p>
                    </div>

                    <div class="info-card" style="margin-top:12px;">
                        <h4 style="margin-top:0; margin-bottom:8px;">Recomendação</h4>
                        <p class="muted-text" style="margin:0;">
                            O Ollama deve estar ativo localmente com os modelos qwen2.5 e qwen2.5vl.
                        </p>
                    </div>
                </div>
                """
            )

        with gr.Column(scale=6, min_width=500):
            gr.Markdown(
                """
                <div class="section-card">
                    <h3 style="margin-top:0;">1. Envie seu PDF</h3>
                    <p class="helper-text">Escolha um arquivo PDF com texto selecionável.</p>
                </div>
                """
            )
            pdf_input = gr.File(label="📄 Arquivo PDF", file_types=[".pdf"], type="filepath")

            gr.Markdown(
                """
                <div class="section-card" style="margin-top:12px;">
                    <h3 style="margin-top:0;">2. Ajuste a velocidade</h3>
                    <p class="helper-text">Defina a velocidade ideal da voz para o seu documento.</p>
                </div>
                """
            )
            speed_input = gr.Slider(
                0.6,
                1.9,
                value=DEFAULT_SPEED,
                step=0.1,
                label="Velocidade da voz",
            )

            gr.Markdown(
                """
                <div class="section-card" style="margin-top:12px;">
                    <h3 style="margin-top:0;">3. Gere o áudio</h3>
                    <p class="helper-text">Faça uma prévia ou gere o áudio completo.</p>
                </div>
                """
            )

            with gr.Row():
                preview_button = gr.Button("🔊 Testar áudio", variant="secondary")
                convert_button = gr.Button("🚀 Gerar áudio completo", variant="primary")

            preview_output = gr.Textbox(
                lines=16,
                label="Texto processado",
                placeholder="A prévia do texto processado aparecerá aqui.",
            )

        with gr.Column(scale=3, min_width=300):
            gr.Markdown(
                """
                <div class="side-card">
                    <h3 style="margin-top:0;">🎧 Prévia e resultado</h3>
                    <p class="helper-text">
                        Acompanhe o status do processamento, ouça a prévia e baixe o arquivo final.
                    </p>
                </div>
                """
            )

            preview_audio_output = gr.Audio(label="Prévia de áudio")
            status_output = gr.Textbox(
                label="Status",
                lines=8,
                placeholder="As mensagens do processamento aparecerão aqui.",
            )
            file_output = gr.File(label="⬇️ Download do áudio")

    gr.Markdown(
        """
        <div class="footer-note">
            Execução local • Interface dark • Qwen + Ollama • Verbalização fiel para conteúdo científico
        </div>
        """
    )

    preview_button.click(
        fn=generate_preview_audio,
        inputs=[pdf_input, speed_input],
        outputs=[preview_audio_output, status_output],
    )

    convert_button.click(
        fn=convert_pdf_to_audio,
        inputs=[pdf_input, speed_input],
        outputs=[preview_output, file_output, status_output],
    )

if __name__ == "__main__":
    demo.launch(inbrowser=True)
