import json
import os

def ensure_parent_dir(file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def load_json(file_path: str, default=None):
    if not os.path.exists(file_path):
        return default
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, file_path: str):
    ensure_parent_dir(file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_text_file(file_path: str, label: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{label} file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        value = f.read().strip()
    if not value:
        raise ValueError(f"{label} file is empty: {file_path}")
    return value