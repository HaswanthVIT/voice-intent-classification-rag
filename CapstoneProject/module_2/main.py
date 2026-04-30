import json
import os
from module_2.nlp_processor import process_text


def load_json(file_path: str):
    print(f"[DEBUG] Loading JSON from: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ==============================
# MAIN (DUAL MODE)
# ==============================
if __name__ == "__main__":
    try:
        print("[DEBUG] Module 2 standalone mode...")

        # ✅ Use ENV if available (pipeline mode)
        input_path = os.environ.get(
            "M1_PATH",
            r"D:\CapstoneProject\module_1\transcript_output.json"
        )

        output_path = os.environ.get(
            "M2_OUTPUT_PATH",
            os.path.join(os.path.dirname(__file__), "module2_output.json")
        )

        module1_output = load_json(input_path)

        print("[DEBUG] Processing text...")
        output = process_text(module1_output)

        save_json(output, output_path)

        print("\n===== MODULE 2 OUTPUT =====\n")
        print(json.dumps(output, indent=2, ensure_ascii=False))
        print(f"\n[DEBUG] Saved to: {output_path}")

    except Exception as e:
        print(f"\n[ERROR] {e}")