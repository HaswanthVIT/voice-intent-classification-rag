# feature_extractor.py

import librosa
import numpy as np
from module_1.config import DIALECT_PROFILE

def extract_customer_features(customer_audio_np, sr, customer_transcript, language):
    duration_sec = float(len(customer_audio_np) / sr) if sr > 0 else 0.0

    # Pitch mean
    try:
        f0, voiced_flag, _ = librosa.pyin(customer_audio_np, fmin=50, fmax=500, sr=sr)
        pitch_mean = float(np.nanmean(f0[voiced_flag])) if np.any(voiced_flag) else 0.0
    except:
        pitch_mean = 0.0

    # Speech rate
    total_words = len(customer_transcript.split())
    speech_rate = float(total_words / (duration_sec / 60)) if duration_sec > 0 else 0.0

    # Pause ratio
    frame_energy = librosa.feature.rms(y=customer_audio_np)[0] if len(customer_audio_np) > 0 else np.array([])
    silence_mask = frame_energy < 0.01 if len(frame_energy) > 0 else np.array([])
    pause_ratio = float(np.sum(silence_mask) / len(silence_mask)) if len(silence_mask) > 0 else 0.0

    # Energy
    raw_energy = float(np.mean(librosa.feature.rms(y=customer_audio_np))) if len(customer_audio_np) > 0 else 0.0

    profile = DIALECT_PROFILE.get(language, DIALECT_PROFILE["en"])
    normalized_energy = raw_energy / profile["energy_norm"]
    normalized_pause_ratio = pause_ratio * profile["pause_weight"]

    return {
        "pitch_mean": round(pitch_mean, 2),
        "speech_rate": round(speech_rate, 2),
        "normalized_energy": round(normalized_energy, 4),
        "normalized_pause_ratio": round(normalized_pause_ratio, 4),
        "customer_speech_duration_sec": round(duration_sec, 2)
    }