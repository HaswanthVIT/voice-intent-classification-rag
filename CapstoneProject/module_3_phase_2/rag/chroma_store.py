from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from ..config import (
    CHROMA_PATH,
    PAST_CALLS_COLLECTION,
    BUSINESS_RULES_COLLECTION,
    EMBED_MODEL_NAME
)

CHROMA_CLIENT = PersistentClient(path=CHROMA_PATH)
EMBED_MODEL = SentenceTransformer(EMBED_MODEL_NAME)

def get_past_calls_collection():
    return CHROMA_CLIENT.get_or_create_collection(PAST_CALLS_COLLECTION)

def get_business_rules_collection():
    return CHROMA_CLIENT.get_or_create_collection(BUSINESS_RULES_COLLECTION)

def embed_text(text: str):
    return EMBED_MODEL.encode(text).tolist()