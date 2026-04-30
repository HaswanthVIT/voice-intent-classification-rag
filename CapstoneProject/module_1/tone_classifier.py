# tone_classifier.py

import librosa
import numpy as np

def classify_tone_from_delta(delta: float) -> str:
    if delta > 20.0:
        return "Enthusiastic"
    if delta < -20.0:
        return "Hesitant"
    return "Confident"

def classify_tone_absolute(audio_np: np.ndarray, energy_norm: float) -> str:
    raw_energy = float(np.mean(librosa.feature.rms(y=audio_np)))
    normalized_energy = raw_energy / energy_norm

    if normalized_energy > 0.65:
        return "Enthusiastic"
    if normalized_energy < 0.25:
        return "Hesitant"
    return "Confident"