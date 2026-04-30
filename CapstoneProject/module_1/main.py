import json
import os
from module_1.config import OUTPUT_JSON, OUTPUT_TXT
from module_1.audio_processor import process_audio


# ==============================
# ENTRY FUNCTION (FOR PIPELINE)
# ==============================
def diarization_stt(audio_path, call_id="CALL_001", forced_language=None):
    return process_audio(
        audio_path=audio_path,
        call_id=call_id,
        forced_language=forced_language
    )


# ==============================
# SAVE OUTPUTS (FIXED)
# ==============================
def save_outputs(results, json_path=None, txt_path=None):
    """
    If paths are provided → pipeline mode
    Else → fallback to default files (standalone mode)
    """

    json_path = json_path or os.environ.get("M1_OUTPUT_PATH", OUTPUT_JSON)
    txt_path = txt_path or os.environ.get("M1_TXT_PATH", OUTPUT_TXT)

    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # ✅ JSON SAVE
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # ✅ TXT SAVE
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Call ID: {results['call_id']}\n")
        f.write(f"Language: {results['language']}\n")
        f.write(f"Customer Speaker: {results.get('customer_speaker')}\n")
        f.write(f"Sales Speaker: {results.get('sales_speaker')}\n")
        f.write(f"Tone: {results['tone']}\n\n")

        f.write("=== CUSTOMER FEATURES ===\n")
        f.write(f"Pitch Mean: {results['pitch_mean']}\n")
        f.write(f"Speech Rate: {results['speech_rate']}\n")
        f.write(f"Normalized Energy: {results['normalized_energy']}\n")
        f.write(f"Normalized Pause Ratio: {results['normalized_pause_ratio']}\n")
        f.write(f"Customer Speech Duration: {results['customer_speech_duration_sec']}\n\n")

        f.write("=== SPEAKER TONES ===\n")
        for spk, info in results["speakers"].items():
            role = results.get("speaker_roles", {}).get(spk, "Unknown")
            f.write(f"{spk} ({role}) -> Tone: {info['tone']} | Delta: {info['energy_delta']}\n")

        f.write("\n=== TRANSCRIPT ===\n")
        for row in results["transcript_segments"]:
            role = results.get("speaker_roles", {}).get(row["speaker"], "Unknown")
            f.write(
                f"[{row['start']} - {row['end']}] "
                f"{row['speaker']} ({role}): {row['text']}\n"
            )

    print(f"\n[DEBUG] Saved JSON -> {json_path}")
    print(f"[DEBUG] Saved TXT  -> {txt_path}")


# ==============================
# STANDALONE RUN
# ==============================
if __name__ == "__main__":
    audio_file = r"C:\Users\naman\Downloads\sample.m4a"

    print("[DEBUG] Running Module 1 standalone...")

    output = diarization_stt(
        audio_path=audio_file,
        call_id="CALL_001",  # ✅ unchanged as you requested
        forced_language=None
    )

    save_outputs(output)

    print("\nFinal Output:")
    print(json.dumps(output, indent=2, ensure_ascii=False))