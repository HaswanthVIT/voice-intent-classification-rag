from backend.mock_modules import process_audio, process_text, process_intent
from backend.db_handler import store_result

def run_pipeline(audio_path, call_id):
    m1 = process_audio(audio_path, call_id)
    m2 = process_text(m1)
    m3 = process_intent(m1, m2)

    store_result(m1, m2, m3)
    return m3