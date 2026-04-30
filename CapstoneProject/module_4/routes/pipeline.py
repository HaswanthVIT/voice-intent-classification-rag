from flask import Blueprint, request, jsonify
from module_4.orchestrator import run_pipeline

pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/run_pipeline", methods=["POST"])
def run():
    try:
        data = request.json
        result = run_pipeline(data["audio_path"], data["call_id"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500