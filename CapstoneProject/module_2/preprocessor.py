# module2/preprocessor.py

import re

FILLERS = [
    " uh ",
    " um ",
    " ah ",
    " er ",
    " hmm ",
    " like ",
    " you know ",
    " actually "
]

def preprocess_transcript(text: str) -> str:
    """
    Lowercase, normalize whitespace, keep '?',
    and remove common fillers.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower().strip()

    # Keep ? but remove most other punctuation except word chars and spaces
    text = re.sub(r"[^\w\s?]", " ", text)

    # Normalize spaces first
    text = re.sub(r"\s+", " ", text)
    text = f" {text} "

    for filler in FILLERS:
        text = text.replace(filler, " ")

    text = re.sub(r"\s+", " ", text).strip()
    return text