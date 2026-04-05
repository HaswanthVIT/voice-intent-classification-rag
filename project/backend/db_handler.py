import sqlite3
import json
from datetime import datetime

DB_PATH = "calls.db"

# -----------------------------
# DB CONNECTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# INIT DB (CREATE TABLE)
# -----------------------------
def init_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS calls (
        call_id TEXT PRIMARY KEY,
        timestamp TEXT,

        transcript TEXT,
        language TEXT,
        pitch_mean REAL,
        speech_rate REAL,
        duration_sec REAL,
        energy_delta REAL,

        transcript_segments TEXT,
        speakers TEXT,

        has_budget INTEGER,
        has_loan INTEGER,
        has_visit INTEGER,
        keyword_norm REAL,
        question_norm REAL,
        engagement_score REAL,
        sentiment TEXT,
        tone TEXT,

        duration_norm REAL,
        speakers_nlp TEXT,

        context_scores TEXT,
        llm_holistic_score REAL,
        signal_score REAL,

        intent_score REAL,
        intent_class TEXT,
        confidence REAL,

        reasoning TEXT,
        evidence_refs TEXT,
        learning_insight TEXT,

        customer_speaker_id TEXT,
        rl_weights_used TEXT,

        outcome TEXT
    )
    """)
    conn.commit()
    conn.close()


# -----------------------------
# STORE RESULT (PIPELINE OUTPUT)
# -----------------------------
def store_result(m1, m2, m3):
    conn = get_db_connection()

    # Preserve outcome
    existing = conn.execute(
        "SELECT outcome FROM calls WHERE call_id = ?",
        (m1["call_id"],)
    ).fetchone()

    outcome = existing["outcome"] if existing else None

    conn.execute("""
    INSERT OR REPLACE INTO calls VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        m1["call_id"],
        datetime.utcnow().isoformat(),

        m1.get("transcript"),
        m1.get("language"),
        m1.get("pitch_mean"),
        m1.get("speech_rate"),
        m1.get("duration_sec"),
        m1.get("energy_delta"),

        # ⚠️ FIXED: MUST check None, not truthy
        json.dumps(m1.get("transcript_segments")) if m1.get("transcript_segments") is not None else None,
        json.dumps(m1.get("speakers")) if m1.get("speakers") is not None else None,

        m2.get("has_budget"),
        m2.get("has_loan"),
        m2.get("has_visit"),
        m2.get("keyword_norm"),
        m2.get("question_norm"),
        m2.get("engagement_score"),
        m2.get("sentiment"),
        m1.get("tone"),

        m2.get("duration_norm"),
        json.dumps(m2.get("speakers_nlp")) if m2.get("speakers_nlp") is not None else None,

        json.dumps(m3.get("context_scores", {})),
        m3.get("llm_holistic_score"),
        m3.get("signal_score"),

        m3.get("intent_score"),
        m3.get("intent_class"),
        m3.get("confidence"),

        json.dumps(m3.get("reasoning", [])),
        json.dumps(m3.get("evidence_refs", [])),
        json.dumps(m3.get("learning_insight", [])),

        m3.get("customer_speaker_id"),
        json.dumps(m3.get("rl_weights_used", {})),

        outcome
    ))

    conn.commit()
    conn.close()