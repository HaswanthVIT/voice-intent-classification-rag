from utils.mappings import TONE_MAP, SENTIMENT_MAP

def build_state_vector(module1_output, module2_output, context_scores):
    s1 = float(module2_output["has_budget"])
    s2 = float(module2_output["has_loan"])
    s3 = float(module2_output["has_visit"])
    s4 = float(module2_output["keyword_norm"])
    s5 = float(module2_output["question_norm"])
    s6 = float(module2_output["engagement_score"])
    s7 = float(TONE_MAP.get(module1_output.get("customer_tone", "Confident"), 0.6))
    s8 = float(SENTIMENT_MAP.get(module2_output.get("sentiment", "neutral"), 0.5))
    s9 = float(context_scores["budget"])
    s10 = float(context_scores["loan"])
    s11 = float(context_scores["visit"])
    s12 = float(context_scores["keyword"])
    s13 = float(context_scores["question"])
    s14 = float(context_scores["engagement"])
    s15 = float(module2_output["duration_norm"])

    return [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]