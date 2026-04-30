# engagement_scorer.py

from module_2.normalizer import keyword_norm, question_norm, duration_norm

def compute_engagement_score(keyword_count: int, question_count: int, duration_sec: float) -> float:
    """
    Composite engagement score based on full-call features.
    Range: 0.0 to 1.0
    """
    keyword_weight  = keyword_norm(keyword_count)
    question_weight = question_norm(question_count)
    duration_weight = duration_norm(duration_sec)

    engagement_score = (
        (0.4 * keyword_weight) +
        (0.4 * question_weight) +
        (0.2 * duration_weight)
    )

    return round(engagement_score, 4)