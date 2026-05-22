#from __future__ import annotations
#from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parents[1]
#VOICE_DIR = BASE_DIR / "voices"
#OUTPUT_DIR = BASE_DIR / "outputs"

#VOICE_MODEL = VOICE_DIR / "pt_BR-voz.onnx"
#VOICE_CONFIG = VOICE_DIR / "pt_BR-voz.onnx.json"

#MAX_CHARS_PREVIEW_TEXT = 7000
#MAX_CHARS_TTS = 150000
#MAX_CHARS_AUDIO_TEST = 900
#DEFAULT_SPEED = 0.9

#VOICE_DIR.mkdir(exist_ok=True)
#OUTPUT_DIR.mkdir(exist_ok=True)


#-----------------------------------------------------------------
#from __future__ import annotations
#from pathlib import Path
#import sys

# Detecta se está rodando como .exe
#if getattr(sys, "frozen", False):
    #BASE_DIR = Path(sys._MEIPASS)
#else:
#    BASE_DIR = Path(__file__).resolve().parents[1]

#VOICE_DIR = BASE_DIR / "voices"
#OUTPUT_DIR = BASE_DIR / "outputs"

#VOICE_MODEL = VOICE_DIR / "pt_BR-voz.onnx"
#VOICE_CONFIG = VOICE_DIR / "pt_BR-voz.onnx.json"

#MAX_CHARS_PREVIEW_TEXT = 7000
#MAX_CHARS_TTS = 150000
#MAX_CHARS_AUDIO_TEST = 900
#DEFAULT_SPEED = 0.9

#VOICE_DIR.mkdir(exist_ok=True)
#OUTPUT_DIR.mkdir(exist_ok=True)

#---------------------------------------
from __future__ import annotations
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parents[1]
    APP_DIR = BASE_DIR

VOICE_DIR = APP_DIR / "voices"
OUTPUT_DIR = APP_DIR / "outputs"

VOICE_MODEL = VOICE_DIR / "pt_BR-voz.onnx"
VOICE_CONFIG = VOICE_DIR / "pt_BR-voz.onnx.json"

MAX_CHARS_PREVIEW_TEXT = 7000
MAX_CHARS_TTS = 150000
MAX_CHARS_AUDIO_TEST = 900
DEFAULT_SPEED = 0.9

VOICE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)