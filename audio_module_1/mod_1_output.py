import json

from audio_preprocess import process_audio
from translate_stt import transcribe_audio, normalize_language
from acoustic_feature_extraction import extract_acoustic_features
from dialect_aware_normalization import dialect_normalization
from tone_classification import run_tone_classification


OUTPUT_JSON = "call_analysis_output.json"


# ------------------------------------------------
# ADD AUDIO FILE PATHS HERE
# ------------------------------------------------
AUDIO_FILES = [
    r"C:\\Users\\naman\\Downloads\\englishtamil.mp3"
]


def run_pipeline(audio_path, call_id):

    # 1️⃣ Preprocess
    meta = process_audio(audio_path)
    processed_audio = meta["processed_file"]

    # 2️⃣ Speech-to-Text
    stt = transcribe_audio(processed_audio)

    transcript = stt["transcript"]
    language = normalize_language(stt["language_detected"])

    # 3️⃣ Acoustic Features
    acoustic = extract_acoustic_features(processed_audio, transcript)

    pitch_mean = acoustic["pitch_mean"]
    speech_rate = acoustic["speech_rate"]
    raw_energy = acoustic["raw_energy"]
    raw_pause_ratio = acoustic["raw_pause_ratio"]

    # 4️⃣ Dialect Normalization
    norm = dialect_normalization(
        raw_energy,
        raw_pause_ratio,
        language
    )

    normalized_energy = norm["normalized_energy"]
    normalized_pause_ratio = norm["normalized_pause_ratio"]

    # 5️⃣ Tone Classification
    tone_result = run_tone_classification(
        processed_audio,
        transcript,
        language,
        pitch_mean,
        speech_rate,
        normalized_energy,
        normalized_pause_ratio
    )

    # 6️⃣ STRICT OUTPUT FORMAT
    final_output = {
        "call_id": call_id,
        "transcript": transcript,
        "language": language,
        "pitch_mean": float(pitch_mean),
        "speech_rate": int(speech_rate),
        "normalized_energy": float(normalized_energy),
        "normalized_pause_ratio": float(normalized_pause_ratio),
        "tone": tone_result["tone"],
        "duration_sec": int(round(tone_result["duration_sec"]))
    }

    return final_output


def main():

    results = []

    for i, audio_path in enumerate(AUDIO_FILES, start=1):

        call_id = f"CALL_{i:03d}"

        print(f"Processing: {audio_path}")

        try:
            result = run_pipeline(audio_path, call_id)
            results.append(result)

        except Exception as e:
            print(f"Error processing {audio_path}: {e}")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("\nProcessing complete.")
    print(f"Output saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()