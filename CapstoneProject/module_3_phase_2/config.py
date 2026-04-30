import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# INPUTS
MODULE1_JSON = os.path.join(PROJECT_ROOT, "module_1", "transcript_output.json")
MODULE2_JSON = os.path.join(PROJECT_ROOT, "module_2", "module2_output.json")

# OUTPUT
MODULE3_OUTPUT_JSON = os.path.join(BASE_DIR, "module3_output.json")

# GEMINI
GEMINI_API_KEY_FILE = os.path.join(PROJECT_ROOT, "api_keys", "gemini_api_key.txt")
GEMINI_MODEL = "gemini-2.5-flash"

# CHROMADB
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chromadb")
PAST_CALLS_COLLECTION = "past_calls"
BUSINESS_RULES_COLLECTION = "business_rules"

# DATA FILES
DATA_DIR = os.path.join(BASE_DIR, "data")
BUSINESS_RULES_JSON = os.path.join(DATA_DIR, "business_rules.json")
SEED_PAST_CALLS_JSON = os.path.join(DATA_DIR, "seed_past_calls.json")
EXPERIENCE_BUFFER_JSON = os.path.join(DATA_DIR, "experience_buffer.json")
RL_POLICY_PATH = os.path.join(DATA_DIR, "rl_policy.pt")

# EMBEDDINGS
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# RL
STATE_DIM = 15
ACTION_DIM = 6
MINOR_FIXED_TONE_WEIGHT = 0.03
MINOR_FIXED_SENTIMENT_WEIGHT = 0.02
LEARNED_WEIGHT_SUM = 0.95

# SCORING
SIGNAL_LAYER_WEIGHT = 0.35
HOLISTIC_LAYER_WEIGHT = 0.65