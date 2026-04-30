# config.py

MODEL_NAME = "medium"
DEVICE = "cpu"

HF_TOKEN_FILE = r"D:\CapstoneProject\api_keys\hf_token.txt"
GEMINI_API_KEY_FILE = r"D:\CapstoneProject\api_keys\gemini_api_key.txt"

OUTPUT_JSON = "transcript_output.json"
OUTPUT_TXT = "transcript_output.txt"

MIN_SEGMENT_DURATION = 1.5
MERGE_GAP_SEC = 0.3
BASELINE_THRESHOLD_SEC = 5.0

DIALECT_PROFILE = {
    "ta": {"energy_norm": 1.2, "pause_weight": 0.8},
    "hi": {"energy_norm": 1.0, "pause_weight": 1.0},
    "en": {"energy_norm": 0.9, "pause_weight": 1.1}
}