DIALECT_PROFILE = {
    "ta": {"energy_norm": 1.2, "pause_weight": 0.8},
    "hi": {"energy_norm": 1.0, "pause_weight": 1.0},
    "en": {"energy_norm": 0.9, "pause_weight": 1.1}
}


def dialect_normalization(raw_energy: float, raw_pause_ratio: float, language: str) -> dict:
    """
    Apply frozen dialect normalization.

    Parameters:
        raw_energy (float)
        raw_pause_ratio (float)
        language (str) -> 'ta', 'hi', 'en'

    Returns:
        normalized features dictionary
    """

    if language not in DIALECT_PROFILE:
        raise ValueError("Unsupported dialect")

    profile = DIALECT_PROFILE[language]

    energy_norm = profile["energy_norm"]
    pause_weight = profile["pause_weight"]

    normalized_energy = round(raw_energy / energy_norm, 2)
    normalized_pause_ratio = round(raw_pause_ratio * pause_weight, 2)

    return {
        "normalized_energy": normalized_energy,
        "normalized_pause_ratio": normalized_pause_ratio,
        "dialect_used": language,
        "mode": "frozen"
    }