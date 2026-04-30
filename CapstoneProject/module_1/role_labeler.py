import json
import time
import google.generativeai as genai

from module_1.config import GEMINI_API_KEY_FILE
from module_1.utils import load_text_file


# -----------------------------
# FALLBACK (RULE-BASED)
# -----------------------------
def fallback_role_detection(transcript_segments):
    speaker_scores = {}

    for seg in transcript_segments:
        spk = seg["speaker"]
        text = seg["text"].lower()

        if spk not in speaker_scores:
            speaker_scores[spk] = {"sales": 0, "customer": 0}

        # SALES indicators
        if any(x in text for x in [
            "price", "offer", "site visit", "we have", "our project",
            "availability", "units", "sqft", "emi", "loan options"
        ]):
            speaker_scores[spk]["sales"] += 1

        # CUSTOMER indicators
        if any(x in text for x in [
            "my budget", "i am looking", "i want", "i saw",
            "i am planning", "can you", "i need", "budget",
            "interested"
        ]):
            speaker_scores[spk]["customer"] += 1

    roles = {}
    for spk, score in speaker_scores.items():
        roles[spk] = "sales" if score["sales"] > score["customer"] else "customer"

    sales_speaker = next((k for k, v in roles.items() if v == "sales"), None)
    customer_speaker = next((k for k, v in roles.items() if v == "customer"), None)

    return {
        "speaker_roles": roles,
        "customer_speaker": customer_speaker,
        "sales_speaker": sales_speaker,
        "confidence": 0.5
    }


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def label_speaker_roles_with_gemini(transcript_segments):

    api_key = load_text_file(GEMINI_API_KEY_FILE, "Gemini API key")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    # 🔥 LIMIT INPUT SIZE (IMPORTANT)
    transcript_segments = transcript_segments[:30]

    conversation_text = "\n".join(
        f"{seg['speaker']}: {seg['text']}"
        for seg in transcript_segments if seg["text"].strip()
    )

    prompt = f"""
You are analyzing a real-estate sales call transcript.

Your task:
1. Identify which speaker is the SALES AGENT.
2. Identify which speaker is the CUSTOMER.

Rules:
- Sales agent explains project, pricing, offers, availability.
- Customer shows interest, asks questions, discusses budget.

Return ONLY valid JSON in this exact format:

{{
  "speaker_roles": {{
    "SPEAKER_00": "sales",
    "SPEAKER_01": "customer"
  }},
  "customer_speaker": "SPEAKER_01",
  "sales_speaker": "SPEAKER_00",
  "confidence": 0.0
}}

STRICT:
- Only JSON
- No markdown
- No explanation

Transcript:
{conversation_text}
"""

    retries = 3

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)

            raw = response.text.strip()

            # Clean markdown if model adds it
            raw = raw.replace("```json", "").replace("```", "").strip()

            parsed = json.loads(raw)

            # Basic validation
            if "speaker_roles" not in parsed:
                raise ValueError("Invalid JSON structure")

            return parsed

        except Exception as e:
            print(f"[Gemini Role Label Attempt {attempt+1}] Error: {e}")

            # Handle quota error
            if "429" in str(e):
                time.sleep(8)

            # Last attempt → fallback
            if attempt == retries - 1:
                print("[Fallback] Using rule-based role detection")
                return fallback_role_detection(transcript_segments)

    return fallback_role_detection(transcript_segments)