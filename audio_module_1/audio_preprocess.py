from pathlib import Path
import librosa
import soundfile as sf


# -----------------------------
# Validation Functions
# -----------------------------

def validate_input(audio_path: str) -> Path:
    if not isinstance(audio_path, str) or not audio_path.strip():
        raise ValueError
    return Path(audio_path)


def validate_file_exists(path: Path) -> None:
    if not path.exists() or not path.is_file():
        raise ValueError


def validate_format(path: Path) -> None:
    if path.suffix.lower() not in [".mp3", ".wav"]:
        raise ValueError


# -----------------------------
# Audio Loading
# -----------------------------

def load_audio(path: Path):
    try:
        y, sr = librosa.load(str(path), sr=None, mono=False)
        if y is None or len(y) == 0:
            raise ValueError
        return y, sr
    except Exception:
        raise ValueError


# -----------------------------
# Preprocessing
# -----------------------------

def convert_to_mono(y):
    if y.ndim > 1:
        y = librosa.to_mono(y)
    return y


def resample_audio(y, sr, target_sr=16000):
    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    return y, sr


# -----------------------------
# Save Processed Audio
# -----------------------------

def save_processed_audio(y, sr, original_path: Path) -> Path:
    script_dir = Path(__file__).parent

    # Create folder if it doesn't exist
    output_folder = script_dir / "processed_audio"
    output_folder.mkdir(exist_ok=True)

    output_name = original_path.stem + "_processed.wav"
    output_path = output_folder / output_name

    sf.write(output_path, y, sr)

    return output_path


# -----------------------------
# Metadata Extraction
# -----------------------------

def extract_metadata(path: Path, y, sr, output_path: Path) -> dict:
    duration = librosa.get_duration(y=y, sr=sr)
    return {
        "file_name": path.name,
        "processed_file": str(output_path),
        "format": ".wav",
        "sample_rate": sr,
        "duration_seconds": round(duration, 2),
        "num_samples": len(y),
        "channels": 1
    }


# -----------------------------
# Main Pipeline Function
# -----------------------------

def process_audio(audio_path: str) -> dict:
    try:
        path = validate_input(audio_path)
        validate_file_exists(path)
        validate_format(path)

        y, sr = load_audio(path)
        y = convert_to_mono(y)
        y, sr = resample_audio(y, sr)

        output_path = save_processed_audio(y, sr, path)

        return extract_metadata(path, y, sr, output_path)

    except Exception:
        raise ValueError("Unsupported audio format or corrupted file")


