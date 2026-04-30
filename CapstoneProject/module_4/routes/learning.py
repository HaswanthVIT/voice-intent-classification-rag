from flask import Blueprint, request, jsonify
from module_4.orchestrator import run_pipeline

learning_bp = Blueprint("learning", __name__)


@learning_bp.route("/learn", methods=["POST"])
def learn():
    """
    Endpoint for RL feedback / learning updates
    """
    data = request.json

    if not data:
        return jsonify({"error": "No input provided"}), 400

    # Expected:
    # {
    #   "call_id": "...",
    #   "feedback_score": 0.8
    # }

    call_id = data.get("call_id")
    feedback_score = data.get("feedback_score")

    if not call_id or feedback_score is None:
        return jsonify({"error": "Missing required fields"}), 400

    # TODO: hook into RL policy update (Module 3)
    # For now just return success

    return jsonify({
        "status": "learning updated",
        "call_id": call_id,
        "feedback_score": feedback_score
    })