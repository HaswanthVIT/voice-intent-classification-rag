# speaker_nlp.py

from module_2.preprocessor import preprocess_transcript
from module_2.keyword_extractor import extract_keywords
from module_2.question_detector import count_questions
from module_2.sentiment_analyzer import get_sentiment
from module_2.normalizer import keyword_norm, question_norm

def assemble_speaker_texts(transcript_segments: list[dict]) -> dict:
    """
    Groups transcript_segments by speaker_id.
    """
    if not transcript_segments:
        return {}

    speaker_texts = {}

    for seg in transcript_segments:
        spk = seg["speaker"]
        text = seg.get("text", "").strip()

        if spk not in speaker_texts:
            speaker_texts[spk] = text
        else:
            speaker_texts[spk] += " " + text

    return speaker_texts

def extract_speaker_nlp(transcript_segments: list[dict]) -> dict:
    """
    Runs keyword, question, and sentiment extraction for EACH speaker.
    """
    if not transcript_segments:
        return {}

    speaker_texts = assemble_speaker_texts(transcript_segments)
    speakers_nlp = {}

    for spk, raw_text in speaker_texts.items():
        text = preprocess_transcript(raw_text)

        keywords, kw_count, has_budget, has_loan, has_visit = extract_keywords(text)
        question_count = count_questions(text)
        sentiment = get_sentiment(text)

        speakers_nlp[spk] = {
            "keywords": keywords,
            "keyword_count": kw_count,
            "has_budget": has_budget,
            "has_loan": has_loan,
            "has_visit": has_visit,
            "question_count": question_count,
            "sentiment": sentiment,
            "keyword_norm": keyword_norm(kw_count),
            "question_norm": question_norm(question_count)
        }

    return speakers_nlp