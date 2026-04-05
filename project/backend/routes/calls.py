from flask import Blueprint, jsonify
import json
from backend.db_handler import get_db_connection

# ✅ Blueprint MUST be defined first
calls_bp = Blueprint("calls", __name__)

# =========================================================
# ✅ GET /calls  → Dashboard (SUMMARY ONLY)
# =========================================================
@calls_bp.route("/calls", methods=["GET"])
def get_calls():
    conn = get_db_connection()

    rows = conn.execute("""
        SELECT * FROM calls
        ORDER BY intent_score DESC, confidence DESC
    """).fetchall()

    conn.close()

    result = []

    for row in rows:
        result.append({
            "call_id": row["call_id"],
            "intent_score": round(row["intent_score"], 2) if row["intent_score"] else None,
            "intent_class": row["intent_class"],
            "confidence": round(row["confidence"], 2) if row["confidence"] else None,
            "language": row["language"],
            "tone": row["tone"],
            "duration_sec": row["duration_sec"],
            "customer_speaker_id": row["customer_speaker_id"],
            "context_scores": json.loads(row["context_scores"]) if row["context_scores"] else {},
            "reasoning": json.loads(row["reasoning"]) if row["reasoning"] else [],
            "outcome": row["outcome"]
        })

    return jsonify(result)


# =========================================================
# ✅ GET /calls/<call_id> → FULL CALL DETAIL (SPEC EXACT)
# =========================================================
@calls_bp.route("/calls/<call_id>", methods=["GET"])
def get_call_by_id(call_id):
    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM calls WHERE call_id = ?", (call_id,)
    ).fetchone()

    conn.close()

    if not row:
        return jsonify({"error": "Call not found"}), 404

    return jsonify({
        "call_id": row["call_id"],

        # ================= MODULE 1 =================
        "transcript": row["transcript"],
        "language": row["language"],
        "pitch_mean": row["pitch_mean"],
        "speech_rate": row["speech_rate"],
        "duration_sec": row["duration_sec"],
        "energy_delta": row["energy_delta"],
        "tone": row["tone"],

        "transcript_segments": json.loads(row["transcript_segments"]) if row["transcript_segments"] else None,
        "speakers": json.loads(row["speakers"]) if row["speakers"] else None,

        # ================= MODULE 2 =================
        "has_budget": row["has_budget"],
        "has_loan": row["has_loan"],
        "has_visit": row["has_visit"],
        "keyword_norm": row["keyword_norm"],
        "question_norm": row["question_norm"],
        "engagement_score": row["engagement_score"],
        "sentiment": row["sentiment"],

        "duration_norm": row["duration_norm"],
        "speakers_nlp": json.loads(row["speakers_nlp"]) if row["speakers_nlp"] else None,

        # ================= MODULE 3 =================
        "context_scores": json.loads(row["context_scores"]) if row["context_scores"] else {},
        "llm_holistic_score": row["llm_holistic_score"],
        "signal_score": row["signal_score"],
        "intent_score": row["intent_score"],
        "intent_class": row["intent_class"],
        "confidence": row["confidence"],
        "reasoning": json.loads(row["reasoning"]) if row["reasoning"] else [],
        "evidence_refs": json.loads(row["evidence_refs"]) if row["evidence_refs"] else [],
        "learning_insight": json.loads(row["learning_insight"]) if row["learning_insight"] else [],

        "customer_speaker_id": row["customer_speaker_id"],
        "rl_weights_used": json.loads(row["rl_weights_used"]) if row["rl_weights_used"] else {},

        # ================= META =================
        "outcome": row["outcome"],
        "timestamp": row["timestamp"]
    })


# =========================================================
# ✅ GET /calls/<call_id>/intent → INTENT ONLY
# =========================================================
@calls_bp.route("/calls/<call_id>/intent", methods=["GET"])
def get_call_intent(call_id):
    conn = get_db_connection()

    row = conn.execute("""
        SELECT intent_score, intent_class, confidence,
               reasoning, evidence_refs
        FROM calls WHERE call_id = ?
    """, (call_id,)).fetchone()

    conn.close()

    if not row:
        return jsonify({"error": "Call not found"}), 404

    return jsonify({
        "intent_score": row["intent_score"],
        "intent_class": row["intent_class"],
        "confidence": row["confidence"],
        "reasoning": json.loads(row["reasoning"]) if row["reasoning"] else [],
        "evidence_refs": json.loads(row["evidence_refs"]) if row["evidence_refs"] else []
    })