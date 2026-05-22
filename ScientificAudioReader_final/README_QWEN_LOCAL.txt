Scientific Audio Reader — versão local com Qwen + Ollama

Arquitetura:
PDF/página -> Qwen2.5-VL -> blocos estruturados -> Qwen2.5 verbalização fiel -> Piper TTS

Pré-requisitos:
1. Instale Ollama
2. Rode:
   ollama pull qwen2.5
   ollama pull qwen2.5vl
3. Confirme que o Ollama está ativo em:
   http://localhost:11434

Execução:
python -m app.ui_gradio

Observação:
Esta versão prioriza fidelidade de leitura para fórmulas e conteúdo científico.
