import os
import torch

from .policy_network import IntentPolicyNetwork
from ..config import RL_POLICY_PATH

def load_or_init_policy():
    model = IntentPolicyNetwork()

    if os.path.exists(RL_POLICY_PATH):
        model.load_state_dict(torch.load(RL_POLICY_PATH, map_location="cpu"))

    model.eval()
    return model

def save_policy(model):
    os.makedirs(os.path.dirname(RL_POLICY_PATH), exist_ok=True)
    torch.save(model.state_dict(), RL_POLICY_PATH)

def compute_effective_reward(predicted_score: float, actual_outcome_score: float) -> float:
    return 1.0 - abs(predicted_score - actual_outcome_score)

def get_rolling_weight_average(buffer, last_n=500):
    if not buffer:
        return {}

    recent = buffer[-last_n:]
    keys = ["budget", "visit", "loan", "keyword", "question", "engagement", "tone", "sentiment"]

    avg = {}
    for k in keys:
        avg[k] = round(sum(item["weights"].get(k, 0.0) for item in recent) / len(recent), 4)

    return avg