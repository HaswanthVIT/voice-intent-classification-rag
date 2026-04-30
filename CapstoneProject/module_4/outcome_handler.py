from module_4.db_handler import get_connection
from module_4.api_client import trigger_rl_update

VALID_OUTCOMES = ["converted", "lost", "followup", "not_interested", "wrong_number"]


def update_outcome(call_id, outcome):
    if outcome not in VALID_OUTCOMES:
        raise ValueError("INVALID_OUTCOME")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE calls SET outcome=? WHERE call_id=?", (outcome, call_id))
    conn.commit()
    conn.close()

    trigger_rl_update(call_id, outcome)