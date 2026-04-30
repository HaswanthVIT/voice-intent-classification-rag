from flask import Blueprint, jsonify
from ..db_handler import create_table, get_connection
import json

# ✅ DEFINE BLUEPRINT (this is what your app is trying to import)
calls_bp = Blueprint("calls", __name__)


@calls_bp.route("/calls", methods=["GET"])
def get_calls():
    create_table()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM calls")
    rows = cur.fetchall()

    columns = [col[0] for col in cur.description]

    result = []
    for row in rows:
        data = dict(zip(columns, row))

        # Deserialize JSON fields
        for key in [
            "transcript_segments",
            "speakers",
            "speakers_nlp",
            "context_scores",
            "state_vector",
            "rl_weights_used"
        ]:
            if data.get(key):
                data[key] = json.loads(data[key])

        result.append(data)

    conn.close()

    # ✅ IMPORTANT: Flask must return response, not raw Python list
    return jsonify(result)