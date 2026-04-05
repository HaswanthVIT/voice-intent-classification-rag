import requests
from backend.db_handler import get_db_connection

def store_call_in_vectordb(call_id, transcript, metadata):
    # Dummy for now (you can connect later)
    print(f"[VectorDB] Stored call {call_id}")


def update_outcome(call_id: str, outcome: str):
    ALLOWED = {"converted","visited","follow_up","no_response","not_interested"}

    if outcome not in ALLOWED:
        return {
            "error_code": "INVALID_OUTCOME",
            "message": f"{outcome} is not allowed"
        }

    conn = get_db_connection()

    # Step 1 — Update DB
    conn.execute(
        "UPDATE calls SET outcome = ? WHERE call_id = ?",
        (outcome, call_id)
    )
    conn.commit()

    row = conn.execute(
        "SELECT * FROM calls WHERE call_id = ?",
        (call_id,)
    ).fetchone()

    conn.close()

    if not row:
        return {
            "error_code": "CALL_NOT_FOUND",
            "message": f"{call_id} not found"
        }

    # Step 2 — Call Module 3 (RL update)
    try:
        requests.post(
            "http://localhost:5001/update_learning",
            json={"call_id": call_id, "outcome": outcome},
            timeout=5
        )
    except Exception as e:
        print("[WARN] RL update failed:", e)

    # Step 3 — Store in Vector DB
    metadata = {
        "call_id": call_id,
        "language": row["language"],
        "tone": row["tone"],
        "intent_class": row["intent_class"],
        "intent_score": row["intent_score"],
        "outcome": outcome
    }

    store_call_in_vectordb(call_id, row["transcript"], metadata)

    return {
        "status": "success",
        "call_id": call_id,
        "outcome": outcome
    }