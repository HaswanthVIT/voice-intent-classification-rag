# module2/question_detector.py

INTERROGATIVE_WORDS = ["what", "why", "how", "when", "where", "can", "is", "do"]

def count_questions(text: str) -> int:
    """
    Counts both explicit '?' and implicit interrogative words.
    """
    if not isinstance(text, str) or not text.strip():
        return 0

    q_count = text.count("?")

    words = text.split()
    for word in words:
        if word.lower() in INTERROGATIVE_WORDS:
            q_count += 1

    return q_count