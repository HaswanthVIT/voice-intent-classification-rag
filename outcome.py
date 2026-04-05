from flask import Blueprint, request, jsonify
from backend.outcome_handler import update_outcome

outcome_bp = Blueprint("outcome", __name__)

@outcome_bp.route("/outcome", methods=["POST"])
def outcome():
    data = request.get_json()

    if not data:
        return jsonify({"error": "INVALID_REQUEST"}), 400

    call_id = data.get("call_id")
    outcome = data.get("outcome")

    if not call_id or not outcome:
        return jsonify({
            "error": "MISSING_FIELDS",
            "message": "call_id and outcome required"
        }), 400

    result = update_outcome(call_id, outcome)

    # If update_outcome returns error_code → send 400
    if "error_code" in result:
        return jsonify(result), 400

    return jsonify(result)