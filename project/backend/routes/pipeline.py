from flask import Blueprint, request, jsonify
from backend.orchestrator import run_pipeline

pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/run_pipeline", methods=["POST"])
def run():
    data = request.get_json()

    if not data:
        return jsonify({"error": "INVALID_REQUEST", "message": "Missing JSON body"}), 400

    audio_path = data.get("audio_path")
    call_id = data.get("call_id")

    if not audio_path or not call_id:
        return jsonify({
            "error": "MISSING_FIELDS",
            "message": "audio_path and call_id are required"
        }), 400

    result = run_pipeline(audio_path, call_id)

    return jsonify(result)