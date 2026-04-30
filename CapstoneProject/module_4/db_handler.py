import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "calls.db")


# -----------------------------
# CONNECTION (SAFE MODE)
# -----------------------------
def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH, timeout=30)

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")

    return conn


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def safe_json_load(value, default):
    try:
        if value is None:
            return default

        if isinstance(value, (list, dict)):
            return value

        value = value.replace("'", '"')  # fix bad JSON
        return json.loads(value)

    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return default


# -----------------------------
# TABLE
# -----------------------------
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS calls (

        call_id TEXT PRIMARY KEY,
        timestamp TEXT,

        transcript TEXT,
        transcript_segments TEXT,

        customer_speaker_id TEXT,

        intent_score REAL,
        intent_class TEXT,
        signal_score REAL,
        confidence REAL,

        has_budget REAL,
        has_loan REAL,
        has_visit REAL,

        context_scores TEXT,
        state_vector TEXT,
        rl_weights_used TEXT,

        reasoning TEXT,
        learning_insight TEXT,
        evidence_refs TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# INSERT FUNCTION
# -----------------------------
def store_result(payload: dict):
    create_table()
    conn = get_connection()
    cur = conn.cursor()

    context = payload.get("context_scores") or {}
    state_vector = payload.get("state_vector") or []
    rl_weights = payload.get("rl_weights_used") or {}

    reasoning = payload.get("reasoning") or []
    learning_insight = payload.get("learning_insight") or []
    evidence_refs = payload.get("evidence_refs") or []

    # FIX: Module 3 outputs "customer_transcript", not "transcript"
    # Fall back through all possible key names so nothing is lost
    transcript = (
        payload.get("transcript")
        or payload.get("customer_transcript")
        or ""
    )

    # FIX: transcript_segments is present in Module 1/2 output;
    # if missing at Module 3 level, it may have been dropped — keep it if present
    segments = (
        payload.get("transcript_segments")
        or []
    )

    cur.execute("""
    INSERT OR REPLACE INTO calls (
        call_id,
        timestamp,

        transcript,
        transcript_segments,

        customer_speaker_id,

        intent_score,
        intent_class,
        signal_score,
        confidence,

        has_budget,
        has_loan,
        has_visit,

        context_scores,
        state_vector,
        rl_weights_used,

        reasoning,
        learning_insight,
        evidence_refs
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        payload.get("call_id"),
        datetime.utcnow().isoformat(),

        transcript,
        json.dumps(segments, ensure_ascii=False),

        payload.get("customer_speaker_id"),

        payload.get("intent_score"),
        payload.get("intent_class"),
        payload.get("signal_score"),
        payload.get("confidence"),

        context.get("budget"),
        context.get("loan"),
        context.get("visit"),

        json.dumps(context, ensure_ascii=False),
        json.dumps(state_vector, ensure_ascii=False),
        json.dumps(rl_weights, ensure_ascii=False),

        json.dumps(reasoning, ensure_ascii=False),
        json.dumps(learning_insight, ensure_ascii=False),
        json.dumps(evidence_refs, ensure_ascii=False)
    ))

    conn.commit()
    conn.close()


# -----------------------------
# FETCH SINGLE CALL
# -----------------------------
def get_call(call_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM calls WHERE call_id = ?", (call_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "call_id": row[0],
        "timestamp": row[1],

        "transcript": row[2],
        "transcript_segments": safe_json_load(row[3], []),

        "customer_speaker_id": row[4],

        "intent_score": row[5],
        "intent_class": row[6],
        "signal_score": row[7],
        "confidence": row[8],

        "has_budget": row[9],
        "has_loan": row[10],
        "has_visit": row[11],

        "context_scores": safe_json_load(row[12], {}),
        "state_vector": safe_json_load(row[13], []),
        "rl_weights_used": safe_json_load(row[14], {}),

        "reasoning": safe_json_load(row[15], []),
        "learning_insight": safe_json_load(row[16], []),
        "evidence_refs": safe_json_load(row[17], [])
    }


# -----------------------------
# FETCH ALL CALLS
# -----------------------------
def get_all_calls():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM calls")
    rows = cur.fetchall()
    conn.close()

    results = []

    for row in rows:
        try:
            results.append({
                "call_id": row[0],
                "timestamp": row[1],

                "transcript": row[2],
                "transcript_segments": safe_json_load(row[3], []),

                "customer_speaker_id": row[4],

                "intent_score": row[5],
                "intent_class": row[6],
                "signal_score": row[7],
                "confidence": row[8],

                "has_budget": row[9],
                "has_loan": row[10],
                "has_visit": row[11],

                "context_scores": safe_json_load(row[12], {}),
                "state_vector": safe_json_load(row[13], []),
                "rl_weights_used": safe_json_load(row[14], {}),

                "reasoning": safe_json_load(row[15], []),
                "learning_insight": safe_json_load(row[16], []),
                "evidence_refs": safe_json_load(row[17], [])
            })
        except Exception as e:
            print("ROW ERROR:", e)

    return results