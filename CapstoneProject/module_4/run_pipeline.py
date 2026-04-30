import sys
import os
import json
import subprocess
import tempfile
import time  # ✅ ADD THIS
from datetime import datetime

sys.path.append(os.path.abspath("."))

from module_1.main import process_audio
from module_2.nlp_processor import process_text as process_nlp
from module_4.db_handler import store_result


def run_pipeline(file_path):
    print("\n--- PIPELINE START ---\n")

    if not os.path.exists(file_path):
        print(f"ERROR: File not found -> {file_path}")
        return {}

    # ---------------- CREATE UNIQUE CALL ID ----------------
    call_id = f"CALL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # ---------------- MODULE 1 ----------------
    print("Running Module 1...")
    m1 = process_audio(file_path)
    m1["call_id"] = call_id

    print("[DEBUG] M1 Transcript length:", len(m1.get("transcript", "")))

    # ---------------- MODULE 2 ----------------
    print("\nRunning Module 2...")
    m2 = process_nlp(m1)

    # ---------------- ⏱️ WAIT 1 MINUTE ----------------
    print("\n⏳ Waiting 60 seconds before Module 3...")
    time.sleep(60)

    # ---------------- TEMP FILE SETUP ----------------
    temp_dir = tempfile.gettempdir()

    temp_m1 = os.path.join(temp_dir, f"m1_{call_id}.json")
    temp_m2 = os.path.join(temp_dir, f"m2_{call_id}.json")
    temp_m3 = os.path.join(temp_dir, f"m3_{call_id}.json")

    # Save M1 + M2
    with open(temp_m1, "w", encoding="utf-8") as f:
        json.dump(m1, f, ensure_ascii=False)

    with open(temp_m2, "w", encoding="utf-8") as f:
        json.dump(m2, f, ensure_ascii=False)

    # ---------------- MODULE 3 (MANDATORY) ----------------
    print("\nRunning Module 3...")

    env = os.environ.copy()
    env["M1_PATH"] = temp_m1
    env["M2_PATH"] = temp_m2
    env["M3_OUTPUT_PATH"] = temp_m3

    result = subprocess.run(
        ["python", "-m", "module_3_phase_2.main"],
        env=env,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError("❌ Module 3 crashed")

    if not os.path.exists(temp_m3):
        raise RuntimeError("❌ Module 3 failed — no output generated")

    with open(temp_m3, "r", encoding="utf-8") as f:
        m3 = json.load(f)

    # ---------------- STORE ----------------
    print("\nStoring in DB...")

    payload = {
        "call_id": call_id,

        "transcript": m1.get("transcript"),

        "customer_speaker_id": m3.get("customer_speaker_id") or m1.get("customer_speaker"),

        "transcript_segments": (
            m2.get("transcript_segments")
            or m1.get("transcript_segments")
            or []
        ),

        "context_scores": m3.get("context_scores") or m2.get("context_scores"),

        "has_budget": m2.get("has_budget"),
        "has_loan": m2.get("has_loan"),
        "has_visit": m2.get("has_visit"),

        "state_vector": m3.get("state_vector"),
        "rl_weights_used": m3.get("rl_weights_used"),

        "intent_score": m3.get("intent_score"),
        "intent_class": m3.get("intent_class"),
        "signal_score": m3.get("signal_score"),
        "confidence": m3.get("confidence"),

        "reasoning": m3.get("reasoning"),
        "learning_insight": m3.get("learning_insight"),
        "evidence_refs": m3.get("evidence_refs"),
    }

    print("[DEBUG] Final transcript length:", len(payload["transcript"]))

    store_result(payload)

    # ---------------- CLEANUP TEMP FILES ----------------
    try:
        os.remove(temp_m1)
        os.remove(temp_m2)
        os.remove(temp_m3)
    except Exception:
        pass

    print("\n--- DONE ✔ Data stored successfully ---\n")

    return payload


# ---------------- RUN FROM CLI ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m module_4.run_pipeline <file_path>")
    else:
        run_pipeline(sys.argv[1])