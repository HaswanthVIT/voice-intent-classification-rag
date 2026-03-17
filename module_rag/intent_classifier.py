# module_rag/intent_classifier.py

def classify_intent(intent_score: float) -> str:
    if 0.80 <= intent_score <= 1.00:
        return "Very Strong"
    elif 0.65 <= intent_score < 0.80:
        return "Strong"
    elif 0.45 <= intent_score < 0.65:
        return "Mild"
    elif 0.25 <= intent_score < 0.45:
        return "Very Mild"
    elif 0.00 <= intent_score < 0.25:
        return "No Chance"
    else:
        raise ValueError("Intent score out of valid range (0.00 – 1.00)")