def validate_module1_output(module1_output: dict) -> dict:
    if not isinstance(module1_output, dict):
        raise ValueError("module1_output must be a dict")

    if not module1_output.get("call_id"):
        raise ValueError("module1_output missing required field: call_id")

    if not module1_output.get("transcript"):
        raise ValueError("module1_output missing required field: transcript")

    module1_output.setdefault("customer_transcript", module1_output.get("transcript", ""))
    module1_output.setdefault("transcript_segments", [])
    module1_output.setdefault("customer_speaker", "UNKNOWN")
    module1_output.setdefault("customer_speaker_id", module1_output.get("customer_speaker", "UNKNOWN"))
    module1_output.setdefault("tone", "Confident")
    module1_output.setdefault("customer_tone", module1_output.get("tone", "Confident"))

    return module1_output

def validate_module2_output(module2_output: dict) -> dict:
    if not isinstance(module2_output, dict):
        raise ValueError("module2_output must be a dict")

    defaults = {
        "has_budget": 0,
        "has_loan": 0,
        "has_visit": 0,
        "keyword_norm": 0.0,
        "question_norm": 0.0,
        "engagement_score": 0.0,
        "duration_norm": 0.5,
        "sentiment": "neutral"
    }

    for k, v in defaults.items():
        module2_output.setdefault(k, v)

    return module2_output