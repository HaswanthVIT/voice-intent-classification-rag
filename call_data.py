from flask import Blueprint, jsonify
from backend.db_handler import get_db_connection
import json

call_data_bp = Blueprint("call_data", __name__)

@call_data_bp.route("/call_data/<call_id>", methods=["GET"])
def get_call_data(call_id):
    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM calls WHERE call_id = ?", (call_id,)
    ).fetchone()

    conn.close()

    if not row:
        return jsonify({"error": "CALL_NOT_FOUND"}), 404

    row = dict(row)

    customer_id = row.get("customer_speaker_id")

    speakers_nlp = json.loads(row["speakers_nlp"]) if row["speakers_nlp"] else None
    speakers = json.loads(row["speakers"]) if row["speakers"] else None
    context_scores = json.loads(row["context_scores"]) if row["context_scores"] else {}

    # ✅ CUSTOMER SIGNAL RESOLUTION (STRICT RULE)
    if customer_id and customer_id not in ["UNKNOWN", "FALLBACK"] and speakers_nlp:
        customer_data = speakers_nlp.get(customer_id, {})

        has_budget = customer_data.get("has_budget")
        has_loan = customer_data.get("has_loan")
        has_visit = customer_data.get("has_visit")
        keyword_norm = customer_data.get("keyword_norm")
        question_norm = customer_data.get("question_norm")
        sentiment = customer_data.get("sentiment")

        tone = None
        if speakers and customer_id in speakers:
            tone = speakers[customer_id].get("tone")

    else:
        # ✅ FALLBACK TO FULL TRANSCRIPT
        has_budget = row.get("has_budget")
        has_loan = row.get("has_loan")
        has_visit = row.get("has_visit")
        keyword_norm = row.get("keyword_norm")
        question_norm = row.get("question_norm")
        sentiment = row.get("sentiment")
        tone = row.get("tone")

    return jsonify({
        "customer_speaker_id": customer_id,
        "has_budget": has_budget,
        "has_loan": has_loan,
        "has_visit": has_visit,
        "keyword_norm": keyword_norm,
        "question_norm": question_norm,
        "engagement_score": row.get("engagement_score"),
        "tone": tone,
        "sentiment": sentiment,
        "duration_norm": row.get("duration_norm"),
        "intent_score": row.get("intent_score"),
        "signal_score": row.get("signal_score"),
        "context_scores": context_scores
    })