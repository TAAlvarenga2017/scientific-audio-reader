from __future__ import annotations
import gradio as gr
from core.config import DEFAULT_SPEED
from app.controller import convert_pdf_to_audio, generate_preview_audio

with gr.Blocks(title="Scientific Audio Reader") as demo:
    gr.Markdown("# Scientific Audio Reader")
    gr.Markdown(
        "Converta PDFs científicos em áudio com uma pipeline estruturada para texto, fórmulas e tabelas."
    )

    with gr.Row():
        pdf_input = gr.File(label="Enviar PDF", file_types=[".pdf"])
        mode_input = gr.Radio(
            choices=["Simples", "Técnico", "Acadêmico"],
            value="Técnico",
            label="Modo de leitura",
        )

    speed_input = gr.Slider(
        minimum=0.6,
        maximum=1.5,
        value=DEFAULT_SPEED,
        step=0.1,
        label="Velocidade da fala",
    )

    with gr.Row():
        preview_button = gr.Button("Testar velocidade")
        convert_button = gr.Button("Gerar áudio completo")

    preview_audio_output = gr.Audio(label="Prévia de áudio")
    status_output = gr.Textbox(label="Status", lines=7)
    preview_output = gr.Textbox(label="Prévia do texto preparado", lines=20)
    file_output = gr.File(label="Baixar áudio gerado")

    preview_button.click(
        fn=generate_preview_audio,
        inputs=[pdf_input, mode_input, speed_input],
        outputs=[preview_audio_output, status_output],
    )

    convert_button.click(
        fn=convert_pdf_to_audio,
        inputs=[pdf_input, mode_input, speed_input],
        outputs=[preview_output, file_output, status_output],
    )

if __name__ == "__main__":
    demo.launch()
