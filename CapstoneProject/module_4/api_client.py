import requests

MODULE3_API = "http://localhost:8000/update_learning"


def trigger_rl_update(call_id, outcome):
    try:
        requests.post(MODULE3_API, json={
            "call_id": call_id,
            "outcome": outcome
        })
    except Exception as e:
        print("RL trigger failed:", e)