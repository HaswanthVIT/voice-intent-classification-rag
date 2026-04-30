def classify_intent(intent_score: float) -> str:
    if intent_score >= 0.70:
        return "High Intent"
    elif intent_score >= 0.45:
        return "Medium Intent"
    return "Low Intent"