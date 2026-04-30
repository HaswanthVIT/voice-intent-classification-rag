# asr.py

import os
import re
import tempfile
from pydub import AudioSegment
import whisper

from module_1.config import MODEL_NAME, DEVICE
from module_1.utils import normalize_language

print(f"Loading Whisper model on: {DEVICE}")
model = whisper.load_model(MODEL_NAME, device=DEVICE)


# -----------------------------
# TEXT CLEANUP HELPERS
# -----------------------------
def clean_translated_text(text: str) -> str:
    """
    Remove prompt leakage / repeated garbage / obvious ASR artifacts.
    """
    if not text:
        return ""

    text = text.strip()

    # Remove leaked instruction prompt text if Whisper hallucinates it
    bad_phrases = [
        "Translate all spoken content into clear English",
        "If the speaker mixes English with Hindi or Tamil",
        "If the speaker mixes Indian words like Hindi or Tamil",
        "convert the full meaning into natural English",
        "Do not keep non-English words unless they are names",
        "Do not keep non-English words unless they are names, brands, or proper nouns",
    ]

    for phrase in bad_phrases:
        text = text.replace(phrase, "")

    # Remove duplicate repeated sentences/phrases
    text = re.sub(r"\b(.+?)\s+\1\b", r"\1", text, flags=re.IGNORECASE)

    # Remove extra whitespace
    text = " ".join(text.split())

    # If text becomes garbage / empty after cleaning
    if len(text.strip()) < 2:
        return ""

    return text.strip()


# -----------------------------
# SINGLE SEGMENT TRANSLATION
# -----------------------------
def transcribe_segment(segment_audio_path: str, language=None):
    """
    Translate a single audio chunk into English using Whisper.
    """
    language = normalize_language(language)

    kwargs = {
        "task": "translate",          # DIRECT TRANSLATION TO ENGLISH
        "beam_size": 5,
        "best_of": 5,
        "temperature": 0.0,
        "condition_on_previous_text": False,   # IMPORTANT: reduces hallucination
        "fp16": False,
        "verbose": False
    }

    if language is not None:
        kwargs["language"] = language

    result = model.transcribe(segment_audio_path, **kwargs)
    text = clean_translated_text(result["text"])

    return {
        "text": text,
        "language": "en"
    }


# -----------------------------
# DIARIZED TRANSCRIPTION
# -----------------------------
def transcribe_diarized_segments(wav_path, diarized_segments, forced_language=None):
    """
    Translate each diarized segment into English.
    """
    audio = AudioSegment.from_wav(wav_path)
    transcript_segments = []

    print("Starting translation by speaker segments...")

    for i, seg in enumerate(diarized_segments):
        start_ms = int(seg["start"] * 1000)
        end_ms = int(seg["end"] * 1000)

        # Skip tiny segments (too error-prone)
        if (end_ms - start_ms) < 2000:
            continue

        chunk = audio[start_ms:end_ms]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_chunk:
            chunk.export(temp_chunk.name, format="wav")
            temp_chunk_path = temp_chunk.name

        try:
            print(
                f"Translating {i+1}/{len(diarized_segments)} | "
                f"{seg['speaker']} | {seg['start']} - {seg['end']}"
            )

            result = transcribe_segment(temp_chunk_path, language=forced_language)
            text = result["text"]

            # Skip empty / garbage outputs
            if not text:
                continue

            transcript_segments.append({
                "speaker": seg["speaker"],
                "start": seg["start"],
                "end": seg["end"],
                "text": text
            })

        finally:
            if os.path.exists(temp_chunk_path):
                os.unlink(temp_chunk_path)

    detected_language = "en"
    full_transcript = " ".join([x["text"] for x in transcript_segments]).strip()

    return transcript_segments, full_transcript, detected_language