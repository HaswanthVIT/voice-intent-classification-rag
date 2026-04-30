from .chroma_store import (
    get_past_calls_collection,
    get_business_rules_collection,
    embed_text
)

def retrieve_context(transcript: str):
    embedding = embed_text(transcript)

    past_col = get_past_calls_collection()
    rules_col = get_business_rules_collection()

    past_results = past_col.query(query_embeddings=[embedding], n_results=3)
    rules_results = rules_col.query(query_embeddings=[embedding], n_results=3)

    similar_calls = []
    if past_results.get("documents") and past_results["documents"][0]:
        for doc, meta in zip(past_results["documents"][0], past_results["metadatas"][0]):
            similar_calls.append({
                "id": meta.get("id", "unknown"),
                "type": "similar_call",
                "intent_label": meta.get("intent_label", "Unknown"),
                "text": doc[:300]
            })

    business_rules = []
    if rules_results.get("documents") and rules_results["documents"][0]:
        for doc, meta in zip(rules_results["documents"][0], rules_results["metadatas"][0]):
            business_rules.append({
                "id": meta.get("id", "unknown"),
                "type": "business_rule",
                "intent_label": meta.get("intent_label", "Unknown"),
                "text": doc
            })

    if not similar_calls:
        similar_calls = [{
            "id": "fallback_call_000",
            "type": "similar_call",
            "intent_label": "Unknown",
            "text": "No similar past calls found yet."
        }]

    if not business_rules:
        business_rules = [{
            "id": "fallback_rule_000",
            "type": "business_rule",
            "intent_label": "Unknown",
            "text": "No business rules found yet."
        }]

    return similar_calls, business_rules