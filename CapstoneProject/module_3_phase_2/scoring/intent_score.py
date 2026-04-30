from ..config import SIGNAL_LAYER_WEIGHT, HOLISTIC_LAYER_WEIGHT

def compute_intent_score(signal_score: float, llm_holistic_score: float) -> float:
    return round(
        SIGNAL_LAYER_WEIGHT * signal_score +
        HOLISTIC_LAYER_WEIGHT * llm_holistic_score,
        4
    )