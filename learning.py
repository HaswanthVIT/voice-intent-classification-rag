from flask import Blueprint, jsonify
from backend.insights import get_learning_summary, get_performance

learning_bp = Blueprint("learning", __name__)

@learning_bp.route("/learning_summary", methods=["GET"])
def learning_summary():
    data = get_learning_summary()
    return jsonify(data)

@learning_bp.route("/performance", methods=["GET"])
def performance():
    data = get_performance()
    return jsonify(data)