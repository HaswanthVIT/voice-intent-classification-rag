# module_rag/reasoning_engine.py

def generate_reasoning(audio_data: dict, nlp_data: dict, intent_score: float) -> list:
    reasons = []

    # 1️⃣ Keywords (strongest signal)
    if nlp_data["keyword_count"] > 0:
        reasons.append(f"{nlp_data['keyword_count']} key buying signals detected")

    # 2️⃣ Questions asked
    if nlp_data["question_count"] > 0:
        reasons.append(f"{nlp_data['question_count']} questions asked")

    # 3️⃣ Engagement reinforcement
    if nlp_data["engagement_score"] >= 0.6:
        reasons.append("High engagement level")
    elif nlp_data["engagement_score"] >= 0.4:
        reasons.append("Moderate engagement level")
    else:
        reasons.append("Low engagement level")

    # 4️⃣ Tone modifier
    tone = audio_data["tone"]
    reasons.append(f"Tone detected: {tone}")

    # 5️⃣ Sentiment modifier
    sentiment = nlp_data["sentiment"]
    reasons.append(f"Sentiment detected: {sentiment}")

    return reasons