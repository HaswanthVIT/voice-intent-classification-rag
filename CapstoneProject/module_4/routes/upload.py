import os
from flask import Blueprint, request, jsonify
from module_4.run_pipeline import run_pipeline

upload_bp = Blueprint("upload", __name__)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    dest = os.path.join(UPLOAD_DIR, file.filename)
    file.save(dest)
    return jsonify({"file_path": os.path.abspath(dest)})


@upload_bp.route("/process", methods=["POST"])
def process_file():
    data = request.get_json()
    file_path = data.get("file_path") if data else None

    if not file_path:
        return jsonify({"error": "file_path is required"}), 400
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found on server"}), 400

    try:
        result = run_pipeline(file_path) or {}  # FIX: guard against None
        return jsonify({
            "call_id":      result.get("call_id", "unknown"),
            "intent_class": result.get("intent_class", "unknown"),
            "status":       "ok"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()  # prints full error in Terminal 1
        return jsonify({"error": str(e)}), 500