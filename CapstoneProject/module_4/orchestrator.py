from module_1.main import process_audio
from module_2.nlp_processor import process_text
from module_3_phase_2.main import process_intent

from module_4.db_handler import store_result


def run_pipeline(audio_path: str, call_id: str):
    """
    STRICT FLOW (DO NOT MODIFY ORDER)
    """

    module1_output = process_audio(audio_path, call_id)
    module2_output = process_text(module1_output)
    module3_output = process_intent(module1_output, module2_output)

    store_result(module1_output, module2_output, module3_output)

    return module3_output