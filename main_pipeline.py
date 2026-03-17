# Module 3 – RAG Intelligence & Intent Scoring
# Version: v1.0
# Embedding Model: all-MiniLM-L6-v2
# Retrieval Top-K: 3
# Python Version: 3.10

from module_rag.scoring_engine import compute_intent_score
from module_rag.intent_classifier import classify_intent
from module_rag.reasoning_engine import generate_reasoning
from module_rag.rag_retriever import RAGRetriever


# ✅ Initialize retriever ONCE (Performance Fix)
retriever = RAGRetriever()


def process_intent(audio_data: dict, nlp_data: dict) -> dict:
    # Step 1: Compute score
    intent_score = compute_intent_score(audio_data, nlp_data)

    # Step 2: Classify
    intent_class = classify_intent(intent_score)

    # Step 3: Reasoning
    reasoning = generate_reasoning(audio_data, nlp_data, intent_score)

    # Step 4: RAG Retrieval (no reloading)
    query_text = f"""
    Language: {audio_data['language']}
    Tone: {audio_data['tone']}
    Keywords: {', '.join(nlp_data['keywords'])}
    Questions: {nlp_data['question_count']}
    Engagement: {nlp_data['engagement_score']}
    Duration: {audio_data['duration_sec']}
    Sentiment: {nlp_data['sentiment']}
    """

    retrieved = retriever.retrieve(query_text)
    evidence_refs = [item["id"] for item in retrieved]

    # Final Strict Output Contract
    return {
        "call_id": audio_data["call_id"],
        "intent_score": intent_score,
        "intent_class": intent_class,
        "confidence": intent_score,  # Frozen rule
        "reasoning": reasoning,
        "evidence_refs": evidence_refs
    }


# -------------------------
# TEST EXECUTION
# -------------------------

if __name__ == "__main__":

    audio_sample = {
        "call_id": "CALL_002",
        "transcript": "Just checking",
        "language": "ta",
        "pitch_mean": 200,
        "speech_rate": 120,
        "normalized_energy": 0.3,
        "normalized_pause_ratio": 0.4,
        "tone": "Hesitant",
        "duration_sec": 40
    }

    nlp_sample = {
        "call_id": "CALL_002",
        "keywords": [],
        "keyword_count": 0,
        "question_count": 0,
        "sentiment": "negative",
        "engagement_score": 0.0
    }

    result = process_intent(audio_sample, nlp_sample)
    print(result)