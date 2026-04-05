def get_learning_summary():
    return {
        "current_weights": {
            "budget": 0.27,
            "visit": 0.35,
            "loan": 0.10,
            "keyword": 0.10,
            "question": 0.09,
            "engagement": 0.07,
            "tone": 0.03,
            "sentiment": 0.02
        },
        "signal_conversion_rates": {
            "budget": 0.62,
            "visit": 0.91,
            "loan": 0.38
        },
        "total_calls_learned": 0,
        "buffer_size": 0,
        "policy_mode": "initial_weights"
    }


def get_performance():
    return {
        "Very Strong": 0.85,
        "Strong": 0.60,
        "Mild": 0.25
    }