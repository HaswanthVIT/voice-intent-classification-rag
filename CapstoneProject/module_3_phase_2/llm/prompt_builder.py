import json

SYSTEM_PROMPT = """
You are an expert real-estate sales call analyst.

You will receive:
1. Customer-only transcript
2. Full speaker-attributed transcript segments for context
3. Customer-attributed structured signals from Module 1 and Module 2
4. Retrieved similar past calls
5. Retrieved business rules

Your tasks:
A) Assign context validation scores from 0.0 to 1.0 for:
   - budget
   - loan
   - visit
   - keyword
   - question
   - engagement

B) Assign one llm_holistic_score from 0.0 to 1.0

C) Return short reasoning and evidence references

Return ONLY valid JSON in this exact schema:
{
  "context_scores": {
    "budget": 0.0,
    "loan": 0.0,
    "visit": 0.0,
    "keyword": 0.0,
    "question": 0.0,
    "engagement": 0.0
  },
  "llm_holistic_score": 0.0,
  "reasoning": ["...", "...", "..."],
  "evidence_refs": ["call_101", "rule_001"],
  "learning_insight": ["...", "..."]
}
"""

def assemble_llm_prompt(module1_output, module2_output, similar_calls, business_rules):
    payload = {
        "customer_transcript": module1_output.get("customer_transcript", ""),
        "transcript_segments": module1_output.get("transcript_segments", []),
        "customer_signals": {
            "has_budget": module2_output.get("has_budget", 0),
            "has_loan": module2_output.get("has_loan", 0),
            "has_visit": module2_output.get("has_visit", 0),
            "keyword_norm": module2_output.get("keyword_norm", 0.0),
            "question_norm": module2_output.get("question_norm", 0.0),
            "engagement_score": module2_output.get("engagement_score", 0.0),
            "sentiment": module2_output.get("sentiment", "neutral"),
            "customer_tone": module1_output.get("customer_tone", "Confident")
        },
        "similar_calls": similar_calls,
        "business_rules": business_rules
    }

    return SYSTEM_PROMPT + "\n\nINPUT:\n" + json.dumps(payload, indent=2, ensure_ascii=False)