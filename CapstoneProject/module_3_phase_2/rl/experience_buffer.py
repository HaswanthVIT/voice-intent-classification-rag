from ..utils.io_utils import load_json, save_json
from ..config import EXPERIENCE_BUFFER_JSON

def load_experience_buffer():
    return load_json(EXPERIENCE_BUFFER_JSON, default=[])

def save_experience_buffer(buffer):
    save_json(buffer, EXPERIENCE_BUFFER_JSON)

def append_experience(call_id, state_vector, weights, intent_score):
    buffer = load_experience_buffer()
    buffer.append({
        "call_id": call_id,
        "state_vector": state_vector,
        "weights": weights,
        "intent_score": intent_score
    })
    save_experience_buffer(buffer)