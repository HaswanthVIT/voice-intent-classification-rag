# module2/normalizer.py

def keyword_norm(keyword_count: int) -> float:
    return round(min(keyword_count / 5, 1.0), 4)

def question_norm(question_count: int) -> float:
    return round(min(question_count / 5, 1.0), 4)

def duration_norm(duration_sec: float) -> float:
    return round(min(duration_sec / 300, 1.0), 4)