from .utils.validator import validate_module1_output, validate_module2_output
from .rag.retriever import retrieve_context
from .llm.context_scorer import call_llm_context_scoring
from .scoring.state_vector import build_state_vector
from .rl.learning import load_or_init_policy
from .rl.bandit import generate_weights_deterministic
from .scoring.signal_score import compute_signal_score
from .scoring.intent_score import compute_intent_score
from .scoring.classifier import classify_intent
from .rl.experience_buffer import append_experience


def process_intent(module1_output: dict, module2_output: dict) -> dict:
    module1_output = validate_module1_output(module1_output)
    module2_output = validate_module2_output(module2_output)

    call_id = module1_output["call_id"]

    customer_speaker_id = module1_output.get("customer_speaker")

    if not customer_speaker_id:
        raise ValueError("customer_speaker not found in module1_output")

    segments = module1_output.get("transcript_segments", [])

    customer_lines = [
        seg["text"]
        for seg in segments
        if seg.get("speaker") == customer_speaker_id
    ]

    customer_transcript = " ".join(customer_lines).strip()

    similar_calls, business_rules = retrieve_context(customer_transcript)
    retrieved_context = similar_calls + business_rules

    llm_result = call_llm_context_scoring(
        module1_output, module2_output, similar_calls, business_rules
    )

    context_scores = llm_result["context_scores"]
    llm_holistic_score = llm_result["llm_holistic_score"]
    reasoning = llm_result["reasoning"]
    evidence_refs = llm_result["evidence_refs"]
    learning_insight = llm_result.get("learning_insight", [])

    state_vector = build_state_vector(module1_output, module2_output, context_scores)

    policy_network = load_or_init_policy()
    rl_weights_used = generate_weights_deterministic(policy_network, state_vector)

    signal_score = compute_signal_score(
        module1_output, module2_output, context_scores, rl_weights_used
    )

    intent_score = compute_intent_score(signal_score, llm_holistic_score)
    intent_class = classify_intent(intent_score)

    append_experience(call_id, state_vector, rl_weights_used, intent_score)

    output = {
        "call_id": call_id,
        "customer_speaker_id": customer_speaker_id,
        "customer_transcript": customer_transcript,
        "retrieved_context": retrieved_context,
        "context_scores": context_scores,
        "llm_holistic_score": llm_holistic_score,
        "state_vector": state_vector,
        "rl_weights_used": rl_weights_used,
        "signal_score": signal_score,
        "intent_score": intent_score,
        "intent_class": intent_class,
        "confidence": intent_score,
        "reasoning": reasoning[:5],
        "evidence_refs": evidence_refs,
        "learning_insight": learning_insight
    }

    return output