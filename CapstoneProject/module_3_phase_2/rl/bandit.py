import torch

from ..config import (
    MINOR_FIXED_TONE_WEIGHT,
    MINOR_FIXED_SENTIMENT_WEIGHT,
    LEARNED_WEIGHT_SUM
)

def generate_weights_deterministic(policy_network, state_vector):
    x = torch.tensor(state_vector, dtype=torch.float32).unsqueeze(0)
    alpha = policy_network(x).squeeze(0)

    mean = alpha / alpha.sum()
    learned = (mean * LEARNED_WEIGHT_SUM).tolist()

    W_t = {
        "budget": learned[0],
        "visit": learned[1],
        "loan": learned[2],
        "keyword": learned[3],
        "question": learned[4],
        "engagement": learned[5],
        "tone": MINOR_FIXED_TONE_WEIGHT,
        "sentiment": MINOR_FIXED_SENTIMENT_WEIGHT
    }

    return W_t