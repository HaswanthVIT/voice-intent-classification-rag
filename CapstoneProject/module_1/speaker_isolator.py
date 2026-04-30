# speaker_isolator.py

import numpy as np
import librosa

from module_1.config import DIALECT_PROFILE, BASELINE_THRESHOLD_SEC
from module_1.tone_classifier import classify_tone_from_delta, classify_tone_absolute

def get_speaker_audio(audio_np, sr, segments, speaker_id):
    chunks = []

    for seg in segments:
        if seg["speaker"] == speaker_id:
            start_sample = int(seg["start"] * sr)
            end_sample = int(seg["end"] * sr)
            chunk = audio_np[start_sample:end_sample]
            if len(chunk) > 0:
                chunks.append(chunk)

    if not chunks:
        return np.array([], dtype=np.float32)

    return np.concatenate(chunks)

def compute_speaker_baselines(audio_np, sr, segments, language):
    profile = DIALECT_PROFILE.get(language, DIALECT_PROFILE["en"])
    energy_norm = profile["energy_norm"]

    speaker_baseline = {}
    speaker_active = {}
    baseline_locked = {}

    unique_speakers = sorted(set(s["speaker"] for s in segments))

    for spk in unique_speakers:
        speaker_baseline[spk] = np.array([], dtype=np.float32)
        speaker_active[spk] = np.array([], dtype=np.float32)
        baseline_locked[spk] = False

    for seg in segments:
        spk = seg["speaker"]
        start_sample = int(seg["start"] * sr)
        end_sample = int(seg["end"] * sr)
        chunk = audio_np[start_sample:end_sample]

        if not baseline_locked[spk]:
            speaker_baseline[spk] = np.concatenate([speaker_baseline[spk], chunk])
            baseline_duration = len(speaker_baseline[spk]) / sr

            if baseline_duration >= BASELINE_THRESHOLD_SEC:
                speaker_baseline[spk] = speaker_baseline[spk][:int(BASELINE_THRESHOLD_SEC * sr)]
                baseline_locked[spk] = True
        else:
            speaker_active[spk] = np.concatenate([speaker_active[spk], chunk])

    results = {}

    for spk in unique_speakers:
        baseline_arr = speaker_baseline[spk]
        active_arr = speaker_active[spk]

        total_speech = (len(baseline_arr) + len(active_arr)) / sr

        if total_speech < 1.0:
            tone = classify_tone_absolute(baseline_arr if len(baseline_arr) > 0 else audio_np, energy_norm)
            results[spk] = {
                "energy_delta": 0.0,
                "tone": tone
            }
            continue

        if len(baseline_arr) == 0:
            results[spk] = {
                "energy_delta": 0.0,
                "tone": "Confident"
            }
            continue

        raw_baseline = float(np.mean(librosa.feature.rms(y=baseline_arr)))
        E_baseline = raw_baseline / energy_norm

        if len(active_arr) < sr * 0.5:
            results[spk] = {
                "energy_delta": 0.0,
                "tone": "Confident"
            }
            continue

        raw_active = float(np.mean(librosa.feature.rms(y=active_arr)))
        E_current = raw_active / energy_norm

        if E_baseline == 0.0:
            energy_delta = 0.0
            tone = "Confident"
        else:
            energy_delta = ((E_current - E_baseline) / E_baseline) * 100
            tone = classify_tone_from_delta(energy_delta)

        results[spk] = {
            "energy_delta": round(energy_delta, 2),
            "tone": tone
        }

    return results