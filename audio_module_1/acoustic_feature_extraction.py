import librosa
import numpy as np
import os


def extract_acoustic_features(audio_path: str, transcript: str) -> dict:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    # ==============================
    # A. Pitch Mean (F0)
    # ==============================
    f0 = librosa.yin(
        y,
        fmin=50,
        fmax=400,
        sr=sr
    )

    voiced_f0 = f0[f0 > 0]  # ignore unvoiced frames
    pitch_mean = float(np.mean(voiced_f0)) if len(voiced_f0) > 0 else 0.0


    # ==============================
    # B. Energy (RMS)
    # ==============================
    rms = librosa.feature.rms(y=y)[0]
    raw_energy = float(np.mean(rms))


    # ==============================
    # C. Speech Rate
    # ==============================
    total_word_count = len(transcript.split())

    if duration > 0:
        speech_rate = total_word_count / (duration / 60)
    else:
        speech_rate = 0


    # ==============================
    # D. Pause Ratio
    # ==============================
    silence_frames = rms < 0.01
    silence_ratio = np.sum(silence_frames) / len(rms)


    return {
        "pitch_mean": round(pitch_mean, 2),
        "raw_energy": raw_energy,
        "speech_rate": int(round(speech_rate)),
        "raw_pause_ratio": round(float(silence_ratio), 2),
        "duration_sec": round(duration, 2)
    }