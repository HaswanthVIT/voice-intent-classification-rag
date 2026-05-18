import random

# -----------------------------
# MODULE 1 MOCK (Audio + Diarization)
# -----------------------------
def process_audio(audio_path: str, call_id: str):
    return {
        "call_id": call_id,
        "transcript": "I am looking for a 2BHK near OMR. My budget is around 50 lakhs. Can I get loan options?",
        "language": "en",
        "pitch_mean": 210.5,
        "speech_rate": 165,
        "duration_sec": 320,
        "energy_delta": 12.4,
        "tone": "Confident",

        # NEW FIELDS
        "transcript_segments": [
            {"speaker": "SPEAKER_00", "text": "Hello, are you looking for a property?"},
            {"speaker": "SPEAKER_01", "text": "Yes, I want a 2BHK near OMR."},
            {"speaker": "SPEAKER_00", "text": "What is your budget?"},
            {"speaker": "SPEAKER_01", "text": "Around 50 lakhs. Can I get loan options?"}
        ],
        "speakers": {
            "SPEAKER_00": {"tone": "Neutral", "energy_delta": 2.1},
            "SPEAKER_01": {"tone": "Confident", "energy_delta": 16.3}
        }
    }


# -----------------------------
# MODULE 2 MOCK (NLP + Speaker-aware)
# -----------------------------
def process_text(module1_output: dict):
    return {
        # CORE FIELDS
        "has_budget": 1,
        "has_loan": 1,
        "has_visit": 0,
        "keyword_norm": 0.4,
        "question_norm": 0.3,
        "engagement_score": 0.65,
        "sentiment": "positive",

        # NEW FIELD
        "duration_norm": min(module1_output["duration_sec"] / 300, 1.0),

        # NEW SPEAKER NLP
        "speakers_nlp": {
            "SPEAKER_00": {
                "has_budget": 0,
                "has_loan": 0,
                "has_visit": 0,
                "question_count": 1,
                "sentiment": "neutral",
                "keyword_norm": 0.2,
                "question_norm": 0.2
            },
            "SPEAKER_01": {
                "has_budget": 1,
                "has_loan": 1,
                "has_visit": 0,
                "question_count": 2,
                "sentiment": "positive",
                "keyword_norm": 0.4,
                "question_norm": 0.5
            }
        }
    }


# -----------------------------
# MODULE 3 MOCK (Intent + RL)
# -----------------------------
def process_intent(module1_output: dict, module2_output: dict):
    return {
        # CORE OUTPUT
        "intent_score": 0.88,
        "intent_class": "Very Strong",
        "confidence": 0.87,

        "reasoning": [
            "Customer explicitly mentioned budget",
            "Loan inquiry indicates buying intent",
            "Multiple questions show engagement"
        ],

        "evidence_refs": ["CALL_1021", "RULE_07"],

        "learning_insight": [
            "Loan + budget combination strongly correlates with conversion"
        ],

        # EXISTING
        "context_scores": {
            "budget": 0.9,
            "visit": 0.4,
            "loan": 0.8,
            "keyword": 0.7,
            "question": 0.6,
            "engagement": 0.7
        },
        "llm_holistic_score": 0.85,
        "signal_score": 0.62,

        # NEW FIELDS
        "customer_speaker_id": "SPEAKER_01",

        "rl_weights_used": {
            "budget": 0.28,
            "visit": 0.33,
            "loan": 0.10,
            "keyword": 0.11,
            "question": 0.09,
            "engagement": 0.07,
            "tone": 0.03,
            "sentiment": 0.02
        }
    }


# -----------------------------
# OPTIONAL MOCK VARIANTS (EDGE CASES)
# -----------------------------

def process_audio_no_diarization(audio_path: str, call_id: str):
    """Simulates diarization failure"""
    return {
        "call_id": call_id,
        "transcript": "Just checking property options.",
        "language": "en",
        "pitch_mean": 180,
        "speech_rate": 140,
        "duration_sec": 60,
        "energy_delta": 3.0,
        "tone": "Neutral",

        # IMPORTANT: NULL CASES
        "transcript_segments": None,
        "speakers": None
    }


def process_text_no_speakers(module1_output: dict):
    """No speaker NLP available"""
    return {
        "has_budget": 0,
        "has_loan": 0,
        "has_visit": 0,
        "keyword_norm": 0.1,
        "question_norm": 0.1,
        "engagement_score": 0.2,
        "sentiment": "neutral",
        "duration_norm": 0.2,

        # IMPORTANT
        "speakers_nlp": None
    }


def process_intent_unknown_customer(module1_output, module2_output):
    """Customer not identified"""
    return {
        "intent_score": 0.2,
        "intent_class": "Very Mild",
        "confidence": 0.5,
        "reasoning": ["Low engagement", "No strong signals"],
        "evidence_refs": [],
        "learning_insight": [],
        "context_scores": {
            "budget": 0.1,
            "visit": 0.0,
            "loan": 0.0,
            "keyword": 0.2,
            "question": 0.1,
            "engagement": 0.2
        },
        "llm_holistic_score": 0.3,
        "signal_score": 0.15,

        # IMPORTANT EDGE CASE
        "customer_speaker_id": "UNKNOWN",

        "rl_weights_used": {
            "budget": 0.25,
            "visit": 0.25,
            "loan": 0.10,
            "keyword": 0.10,
            "question": 0.10,
            "engagement": 0.10,
            "tone": 0.05,
            "sentiment": 0.05
        }
    }