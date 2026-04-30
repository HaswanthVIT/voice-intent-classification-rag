# audio_processor.py

import os
import librosa

from module_1.config import HF_TOKEN_FILE, MIN_SEGMENT_DURATION, MERGE_GAP_SEC
from module_1.utils import load_text_file, convert_to_wav, normalize_language
from module_1.diarizer import run_diarization, merge_short_segments
from module_1.asr import transcribe_diarized_segments
from module_1.role_labeler import label_speaker_roles_with_gemini
from module_1.speaker_isolator import compute_speaker_baselines, get_speaker_audio
from module_1.feature_extractor import extract_customer_features

def process_audio(audio_path: str, call_id: str = "CALL_001", forced_language: str = None):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    hf_token = load_text_file(HF_TOKEN_FILE, "Hugging Face token")

    print("Converting audio to WAV...")
    wav_path = convert_to_wav(audio_path)
    print(f"Temporary WAV created: {wav_path}")

    try:
        audio_np, sr = librosa.load(wav_path, sr=16000, mono=True)
        duration_sec = float(librosa.get_duration(y=audio_np, sr=sr))

        # Step 1: Diarization
        diarized_segments = run_diarization(wav_path, hf_token)
        diarized_segments = merge_short_segments(
            diarized_segments,
            min_duration=MIN_SEGMENT_DURATION,
            max_gap=MERGE_GAP_SEC
        )

        # Step 2: Segment-wise ASR
        transcript_segments, full_transcript, detected_language = transcribe_diarized_segments(
            wav_path,
            diarized_segments,
            forced_language=forced_language
        )

        language = normalize_language(detected_language if forced_language is None else forced_language)

        # Step 3: Gemini role labeling
        role_info = label_speaker_roles_with_gemini(transcript_segments)
        customer_speaker = role_info.get("customer_speaker")

        # Step 4: Customer-only audio + transcript
        customer_audio_np = get_speaker_audio(audio_np, sr, diarized_segments, customer_speaker) if customer_speaker else audio_np
        customer_transcript = " ".join(
            [seg["text"] for seg in transcript_segments if seg["speaker"] == customer_speaker]
        ).strip() if customer_speaker else full_transcript

        # Step 5: Customer-only acoustic features
        customer_features = extract_customer_features(
            customer_audio_np=customer_audio_np,
            sr=sr,
            customer_transcript=customer_transcript,
            language=language
        )

        # Step 6: Per-speaker cumulative baseline tone
        speakers = compute_speaker_baselines(audio_np, sr, diarized_segments, language)

        # Top-level tone = customer tone
        top_level_tone = speakers.get(customer_speaker, {}).get("tone", "Confident") if customer_speaker else "Confident"

        final_output = {
            "call_id": call_id,
            "transcript": full_transcript,
            "language": language,
            "pitch_mean": customer_features["pitch_mean"],
            "speech_rate": customer_features["speech_rate"],
            "normalized_energy": customer_features["normalized_energy"],
            "normalized_pause_ratio": customer_features["normalized_pause_ratio"],
            "customer_speech_duration_sec": customer_features["customer_speech_duration_sec"],
            "tone": top_level_tone,
            "duration_sec": round(duration_sec, 2),
            "speakers": speakers,
            "transcript_segments": transcript_segments,
            "speaker_roles": role_info.get("speaker_roles", {}),
            "customer_speaker": role_info.get("customer_speaker"),
            "sales_speaker": role_info.get("sales_speaker"),
            "role_label_confidence": role_info.get("confidence", "unknown")
        }

        print("Transcription + diarization completed.")
        return final_output

    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)