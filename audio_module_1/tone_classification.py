import librosa
import numpy as np
import os


# ============================================================
# SILENT CALL DETECTION
# ============================================================

def detect_silent_call(audio_path: str):
    """
    Detect if the entire call is silent.
    Silence defined as RMS < 0.01 for all frames.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    rms = librosa.feature.rms(y=y)[0]
    threshold = 0.01

    if np.all(rms < threshold):
        return {
            "call_id": "...",
            "transcript": "",
            "language": "en",
            "pitch_mean": 0.0,
            "speech_rate": 0,
            "normalized_energy": 0.0,
            "normalized_pause_ratio": 1.0,
            "tone": "Neutral",
            "duration_sec": round(duration, 2)
        }

    return None


# ============================================================
# STRICT RULE-BASED TONE CLASSIFICATION
# ============================================================

def classify_tone(
    normalized_energy: float,
    speech_rate: int,
    normalized_pause_ratio: float,
    duration_sec: float
) -> str:
    """
    Deterministic tone classification.

    Order of evaluation:
    1. Enthusiastic
    2. Confident
    3. Hesitant
    4. Neutral
    """

    # EDGE CASE: Very short call
    if duration_sec < 5:
        return "Neutral"

    # 1️⃣ Enthusiastic
    if normalized_energy > 0.85 and speech_rate > 170:
        return "Enthusiastic"

    # 2️⃣ Confident
    if (
        0.6 <= normalized_energy <= 0.85
        and 140 <= speech_rate <= 180
        and normalized_pause_ratio < 0.15
    ):
        return "Confident"

    # 3️⃣ Hesitant
    if normalized_pause_ratio > 0.20 or speech_rate < 120:
        return "Hesitant"

    # 4️⃣ Default
    return "Neutral"


# ============================================================
# FINAL TONE PIPELINE
# ============================================================

def run_tone_classification(
    audio_path: str,
    transcript: str,
    language: str,
    pitch_mean: float,
    speech_rate: int,
    normalized_energy: float,
    normalized_pause_ratio: float
) -> dict:
    """
    Final tone classification step.
    """

    # Check silent call
    silent_result = detect_silent_call(audio_path)
    if silent_result is not None:
        return silent_result

    # Load audio only to compute duration
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    tone = classify_tone(
        normalized_energy=normalized_energy,
        speech_rate=speech_rate,
        normalized_pause_ratio=normalized_pause_ratio,
        duration_sec=duration
    )

    return {
        "call_id": "...",
        "transcript": transcript,
        "language": language,
        "pitch_mean": pitch_mean,
        "speech_rate": speech_rate,
        "normalized_energy": normalized_energy,
        "normalized_pause_ratio": normalized_pause_ratio,
        "tone": tone,
        "duration_sec": round(duration, 2)
    }

