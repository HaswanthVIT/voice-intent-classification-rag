import whisper
import os
import torch

# ==============================
# CONFIGURATION
# ==============================
MODEL_NAME = "medium"

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading model on: {device}")

model = whisper.load_model(MODEL_NAME, device=device)


# ==============================
# LANGUAGE NORMALIZATION
# ==============================
def normalize_language(lang: str) -> str:
    allowed = {"ta", "hi", "en"}
    return lang if lang in allowed else "en"

# ==============================
# TRANSCRIBE FUNCTION
# ==============================
def transcribe_audio(audio_path: str) -> dict:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print("Starting transcription...")

    result = model.transcribe(
        audio_path,

        task="transcribe",
        language="en",

        beam_size=5,
        best_of=5,
        temperature=0.0,

        condition_on_previous_text=True,
        suppress_tokens=[],

        initial_prompt=(
            "The speech may contain English mixed with Indian languages "
            "like Hindi or Tamil. Do not translate. "
            "Write everything exactly as spoken. "
            "If non-English words are spoken, write them in Roman script "
            "like mujhe, enakku, vanakkam, pannunga, etc."
        ),

        fp16=(device == "cuda"),
        verbose=True
    )

    print("Transcription completed.")

    return {
        "transcript": result["text"].strip(),
        "language_detected": result.get("language"),
        "mode": "max_accuracy_mixed_language",
        "model_used": MODEL_NAME,
        "device_used": device
    }

