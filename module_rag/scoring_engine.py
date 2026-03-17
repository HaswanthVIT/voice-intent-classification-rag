# module_rag/scoring_engine.py

REQUIRED_AUDIO_FIELDS = [
    "call_id",
    "transcript",
    "language",
    "pitch_mean",
    "speech_rate",
    "normalized_energy",
    "normalized_pause_ratio",
    "tone",
    "duration_sec"
]

REQUIRED_NLP_FIELDS = [
    "call_id",
    "keywords",
    "keyword_count",
    "question_count",
    "sentiment",
    "engagement_score"
]


def structured_error(error_code: str, message: str) -> dict:
    return {
        "error_code": error_code,
        "module": "module_rag",
        "message": message
    }


def validate_inputs(audio_data: dict, nlp_data: dict) -> None:
    # Type check
    if not isinstance(audio_data, dict) or not isinstance(nlp_data, dict):
        raise ValueError(
            structured_error(
                "INVALID_INPUT_SCHEMA",
                "Inputs must be dictionaries"
            )
        )

    # Required fields check
    for field in REQUIRED_AUDIO_FIELDS:
        if field not in audio_data:
            raise ValueError(
                structured_error(
                    "INVALID_INPUT_SCHEMA",
                    f"Missing audio field: {field}"
                )
            )

    for field in REQUIRED_NLP_FIELDS:
        if field not in nlp_data:
            raise ValueError(
                structured_error(
                    "INVALID_INPUT_SCHEMA",
                    f"Missing nlp field: {field}"
                )
            )

    # CALL_ID match enforcement
    if audio_data["call_id"] != nlp_data["call_id"]:
        raise ValueError(
            structured_error(
                "CALL_ID_MISMATCH",
                "call_id mismatch between audio_data and nlp_data"
            )
        )
    

# -----------------------------
# FROZEN WEIGHT DEFINITIONS
# -----------------------------

BASE_WEIGHTS = {
    "keyword": 0.30,
    "questions": 0.20,
    "engagement": 0.25,
    "tone": 0.15,
    "sentiment": 0.10
}

TONE_SCORE = {
    "Confident": 1.0,
    "Enthusiastic": 0.9,
    "Neutral": 0.6,
    "Hesitant": 0.3
}

SENTIMENT_SCORE = {
    "positive": 1.0,
    "neutral": 0.6,
    "negative": 0.2
}


def compute_intent_score(audio_data: dict, nlp_data: dict) -> float:
    validate_inputs(audio_data, nlp_data)

    keyword_count = nlp_data["keyword_count"]
    question_count = nlp_data["question_count"]
    engagement_score = nlp_data["engagement_score"]
    tone_label = audio_data["tone"]
    sentiment_label = nlp_data["sentiment"]

    tone_score = TONE_SCORE.get(tone_label, 0.0)
    sentiment_score = SENTIMENT_SCORE.get(sentiment_label, 0.0)

    keyword_component = min(keyword_count / 5, 1.0) * BASE_WEIGHTS["keyword"]
    question_component = min(question_count / 5, 1.0) * BASE_WEIGHTS["questions"]
    engagement_component = engagement_score * BASE_WEIGHTS["engagement"]
    tone_component = tone_score * BASE_WEIGHTS["tone"]
    sentiment_component = sentiment_score * BASE_WEIGHTS["sentiment"]

    intent_score = round(
        keyword_component +
        question_component +
        engagement_component +
        tone_component +
        sentiment_component,
        2
    )

    return intent_score