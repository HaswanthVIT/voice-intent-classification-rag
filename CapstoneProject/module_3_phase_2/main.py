import json
import os

from .config import MODULE1_JSON, MODULE2_JSON, MODULE3_OUTPUT_JSON
from .utils.io_utils import load_json, save_json
from .rag.seed_rules import seed_all
from .intent_processor import process_intent


def main():
    print("[DEBUG] Seeding ChromaDB if empty...")
    seed_all()

    # ✅ USE ENV VARIABLES (CRITICAL FIX)
    m1_path = os.environ.get("M1_PATH", MODULE1_JSON)
    m2_path = os.environ.get("M2_PATH", MODULE2_JSON)
    m3_output_path = os.environ.get("M3_OUTPUT_PATH", MODULE3_OUTPUT_JSON)

    print(f"[DEBUG] Loading Module 1 from: {m1_path}")
    module1_output = load_json(m1_path)

    print(f"[DEBUG] Loading Module 2 from: {m2_path}")
    module2_output = load_json(m2_path)

    if module1_output is None:
        raise FileNotFoundError(f"Module 1 output not found: {m1_path}")

    if module2_output is None:
        raise FileNotFoundError(f"Module 2 output not found: {m2_path}")

    print("[DEBUG] Running Module 3 intent processor...")
    result = process_intent(module1_output, module2_output)

    # ✅ SAVE TO TEMP PATH (NOT FIXED FILE)
    save_json(result, m3_output_path)

    print("\n===== MODULE 3 OUTPUT =====\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print(f"\n[DEBUG] Saved output to: {m3_output_path}")


if __name__ == "__main__":
    main()