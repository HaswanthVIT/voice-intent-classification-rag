# module2/validator.py

REQUIRED_KEYS = ["call_id", "transcript", "language", "duration_sec"]

def validate_module1_output(module1_output: dict) -> None:
    """
    Raises ValueError with spec-aligned message if schema invalid.
    """
    if not isinstance(module1_output, dict):
        raise ValueError("Input does not match required schema")

    for key in REQUIRED_KEYS:
        if key not in module1_output:
            raise ValueError("Input does not match required schema")

    if not isinstance(module1_output["transcript"], str):
        raise ValueError("Input does not match required schema")

    if not isinstance(module1_output["language"], str):
        raise ValueError("Input does not match required schema")

    if not isinstance(module1_output["duration_sec"], (int, float)):
        raise ValueError("Input does not match required schema")

    transcript_segments = module1_output.get("transcript_segments", [])
    if transcript_segments is not None and not isinstance(transcript_segments, list):
        raise ValueError("Input does not match required schema")