from ..utils.mappings import TONE_MAP, SENTIMENT_MAP

def compute_signal_score(module1_output, module2_output, context_scores, W_t):
    tone_numeric = TONE_MAP.get(module1_output.get("customer_tone", "Confident"), 0.6)
    sentiment_numeric = SENTIMENT_MAP.get(module2_output.get("sentiment", "neutral"), 0.5)

    signal_score = (
        W_t["budget"]     * module2_output["has_budget"]      * context_scores["budget"] +
        W_t["visit"]      * module2_output["has_visit"]       * context_scores["visit"] +
        W_t["loan"]       * module2_output["has_loan"]        * context_scores["loan"] +
        W_t["keyword"]    * module2_output["keyword_norm"]    * context_scores["keyword"] +
        W_t["question"]   * module2_output["question_norm"]   * context_scores["question"] +
        W_t["engagement"] * module2_output["engagement_score"]* context_scores["engagement"] +
        W_t["tone"]       * tone_numeric +
        W_t["sentiment"]  * sentiment_numeric
    )

    return round(float(signal_score), 4)