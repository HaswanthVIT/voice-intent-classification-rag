import json
import re
import google.generativeai as genai

from ..config import GEMINI_API_KEY_FILE
from ..utils.io_utils import load_text_file
from .prompt_builder import assemble_llm_prompt


def fallback_scoring():
    return {
        "context_scores": {
            "budget": 0.5,
            "loan": 0.5,
            "visit": 0.5,
            "keyword": 0.5,
            "question": 0.5,
            "engagement": 0.5
        },
        "llm_holistic_score": 0.5,
        "reasoning": [
            "Fallback scoring activated due to LLM failure.",
            "Neutral context assumptions were applied.",
            "No contextual boost or suppression was used."
        ],
        "evidence_refs": [],
        "learning_insight": ["LLM unavailable during scoring."]
    }


def safe_parse_json(text):
    try:
        # Step 1: remove markdown wrappers
        text = text.replace("```json", "").replace("```", "").strip()

        # Step 2: find first { and last }
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return None

        json_str = text[start:end + 1]

        # Step 3: fix trailing commas (VERY common in LLM output)
        json_str = re.sub(r",\s*}", "}", json_str)
        json_str = re.sub(r",\s*]", "]", json_str)

        return json.loads(json_str)

    except Exception as e:
        print("[JSON ERROR]", e)
        return None


def call_llm_context_scoring(module1_output, module2_output, similar_calls, business_rules):
    try:
        api_key = load_text_file(GEMINI_API_KEY_FILE, "Gemini API key")

        # OLD SDK setup
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = assemble_llm_prompt(
            module1_output, module2_output, similar_calls, business_rules
        )

        response = model.generate_content(prompt)

        raw_text = None

        # response.text usually works here
        if hasattr(response, "text") and response.text:
            raw_text = response.text
        else:
            try:
                raw_text = response.candidates[0].content.parts[0].text
            except Exception:
                raw_text = None

        if not raw_text:
            raise ValueError("Empty response from Gemini")

        parsed = safe_parse_json(raw_text)

        if not parsed:
            print("[DEBUG] Raw LLM output:")
            print(raw_text)
            raise ValueError("Invalid JSON response from Gemini")

        # safer score handling
        score = parsed.get("llm_holistic_score", 0.5)
        try:
            score = float(score)
        except:
            score = 0.5
        score = max(0.0, min(1.0, score))

        return {
            "context_scores": parsed.get("context_scores", fallback_scoring()["context_scores"]),
            "llm_holistic_score": score,
            "reasoning": parsed.get("reasoning", fallback_scoring()["reasoning"]),
            "evidence_refs": parsed.get("evidence_refs", []),
            "learning_insight": parsed.get("learning_insight", [])
        }

    except Exception as e:
        print(f"[WARN] LLM scoring failed: {e}")
        return fallback_scoring()