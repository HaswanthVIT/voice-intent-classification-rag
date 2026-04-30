# utils.py

import os
import tempfile
from pydub import AudioSegment

def load_text_file(file_path: str, label: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{label} file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        value = f.read().strip()

    if not value:
        raise ValueError(f"{label} file is empty: {file_path}")

    return value

def normalize_language(lang):
    allowed = {"ta", "hi", "en", None}
    return lang if lang in allowed else "en"

def convert_to_wav(input_path: str) -> str:
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)

    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    temp_wav.close()

    return temp_wav.name