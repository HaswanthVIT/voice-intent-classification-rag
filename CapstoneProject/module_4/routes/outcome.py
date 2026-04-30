from flask import Blueprint, request, jsonify
from module_4.outcome_handler import update_outcome

outcome_bp = Blueprint("outcome", __name__)

@outcome_bp.route("/update_outcome", methods=["POST"])
def update():
    data = request.json
    update_outcome(data["call_id"], data["outcome"])
    return jsonify({"status": "updated"})