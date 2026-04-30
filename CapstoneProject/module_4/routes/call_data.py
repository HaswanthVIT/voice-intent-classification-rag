from flask import Blueprint, jsonify
from module_4.db_handler import get_connection
import json

call_data_bp = Blueprint("call_data", __name__)

@call_data_bp.route("/call_data/<call_id>", methods=["GET"])
def get_call_data(call_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT state_vector, intent_score FROM calls WHERE call_id=?", (call_id,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "state_vector": json.loads(row[0]) if row[0] else [],
        "intent_score": row[1]
    })