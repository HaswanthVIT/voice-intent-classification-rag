from ..utils.io_utils import load_json
from ..config import BUSINESS_RULES_JSON, SEED_PAST_CALLS_JSON
from ..rag.chroma_store import (
    get_past_calls_collection,
    get_business_rules_collection,
    embed_text
)

def seed_business_rules():
    rules = load_json(BUSINESS_RULES_JSON, default=[])
    col = get_business_rules_collection()

    if col.count() > 0:
        return

    for item in rules:
        col.add(
            ids=[item["id"]],
            documents=[item["text"]],
            metadatas=[{
                "id": item["id"],
                "intent_label": item.get("intent_label", "Unknown")
            }],
            embeddings=[embed_text(item["text"])]
        )

def seed_past_calls():
    calls = load_json(SEED_PAST_CALLS_JSON, default=[])
    col = get_past_calls_collection()

    if col.count() > 0:
        return

    for item in calls:
        col.add(
            ids=[item["id"]],
            documents=[item["text"]],
            metadatas=[{
                "id": item["id"],
                "intent_label": item.get("intent_label", "Unknown")
            }],
            embeddings=[embed_text(item["text"])]
        )

def seed_all():
    seed_business_rules()
    seed_past_calls()