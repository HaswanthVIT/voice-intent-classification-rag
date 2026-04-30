# nlp_processor.py

from module_2.validator import validate_module1_output
from module_2.preprocessor import preprocess_transcript
from module_2.keyword_extractor import extract_keywords
from module_2.question_detector import count_questions
from module_2.sentiment_analyzer import get_sentiment
from module_2.engagement_scorer import compute_engagement_score
from module_2.speaker_nlp import extract_speaker_nlp
from module_2.normalizer import keyword_norm, question_norm, duration_norm

def process_text(module1_output: dict) -> dict:
    """
    Main entry point for Module 2.

    Receives full Module 1 output dict.
    Returns structured NLP feature dict for Module 3.
    """
    try:
        validate_module1_output(module1_output)

        call_id = module1_output["call_id"]
        transcript = module1_output["transcript"]
        language = module1_output["language"]
        duration_sec = module1_output["duration_sec"]
        transcript_segs = module1_output.get("transcript_segments", [])

        # ── FULL TRANSCRIPT PROCESSING ───────────────────────────────
        full_clean = preprocess_transcript(transcript)

        keywords, keyword_count, has_budget, has_loan, has_visit = extract_keywords(full_clean)
        question_count = count_questions(full_clean)
        sentiment = get_sentiment(full_clean)

        engagement_score = compute_engagement_score(
            keyword_count=keyword_count,
            question_count=question_count,
            duration_sec=duration_sec
        )

        kw_norm = keyword_norm(keyword_count)
        q_norm = question_norm(question_count)
        dur_norm = duration_norm(duration_sec)

        # ── SPEAKER-LEVEL NLP ───────────────────────────────────────
        speakers_nlp = extract_speaker_nlp(transcript_segs)

        # ── FINAL OUTPUT ────────────────────────────────────────────
        output = {
            "call_id": call_id,
            "transcript": transcript,
            "language": language,
            "duration_sec": round(float(duration_sec), 2),

            "clean_transcript": full_clean,

            "keywords": keywords,
            "keyword_count": keyword_count,
            "has_budget": has_budget,
            "has_loan": has_loan,
            "has_visit": has_visit,

            "question_count": question_count,
            "sentiment": sentiment,
            "engagement_score": engagement_score,

            "keyword_norm": kw_norm,
            "question_norm": q_norm,
            "duration_norm": dur_norm,

            "transcript_segments": transcript_segs,
            "speakers_nlp": speakers_nlp,

            # Passed through unchanged if present
            "tone": module1_output.get("tone"),
            "pitch_mean": module1_output.get("pitch_mean"),
            "speech_rate": module1_output.get("speech_rate"),
            "normalized_energy": module1_output.get("normalized_energy"),
            "normalized_pause_ratio": module1_output.get("normalized_pause_ratio")
        }

        return output

    except Exception:
        return {
            "error_code": "INVALID_INPUT_SCHEMA",
            "module": "module_nlp",
            "message": "Input does not match required schema"
        }