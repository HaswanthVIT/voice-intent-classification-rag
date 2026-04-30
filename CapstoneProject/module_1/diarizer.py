# diarizer.py

import soundfile as sf
import torch
from pyannote.audio import Pipeline


def run_diarization(wav_path: str, hf_token: str):
    """
    Run speaker diarization and return cleaned speaker segments.
    """
    print("Loading diarization pipeline...")

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token
    )

    print("Loading waveform manually using soundfile...")
    waveform, sample_rate = sf.read(wav_path)

    waveform = torch.tensor(waveform, dtype=torch.float32)

    # Convert to [channels, time]
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)
    else:
        waveform = waveform.T

    print("Running diarization...")
    diarization = pipeline({
        "waveform": waveform,
        "sample_rate": sample_rate
    })

    segments = []
    annotation = diarization.speaker_diarization if hasattr(diarization, "speaker_diarization") else diarization

    for turn, _, speaker in annotation.itertracks(yield_label=True):
        segments.append({
            "start": round(turn.start, 3),
            "end": round(turn.end, 3),
            "speaker": speaker
        })

    # Post-process for stability
    segments = merge_short_segments(segments, min_duration=2.0, max_gap=0.8)
    segments = smooth_speaker_flips(segments, min_flip_duration=1.2)

    return segments


def merge_short_segments(segments, min_duration=2.0, max_gap=0.8):
    """
    Merge adjacent same-speaker chunks and remove tiny fragments.
    """
    if not segments:
        return []

    merged = [segments[0].copy()]

    for seg in segments[1:]:
        last = merged[-1]
        gap = seg["start"] - last["end"]

        # Merge if same speaker and close enough
        if seg["speaker"] == last["speaker"] and gap <= max_gap:
            last["end"] = seg["end"]
        else:
            merged.append(seg.copy())

    # Filter out very tiny segments
    final = []
    for seg in merged:
        duration = seg["end"] - seg["start"]
        if duration >= min_duration:
            final.append(seg)

    return final


def smooth_speaker_flips(segments, min_flip_duration=1.2):
    """
    Fix A-B-A micro-flips where middle segment is too short.
    Example:
        SPEAKER_00 (long)
        SPEAKER_01 (0.7 sec)
        SPEAKER_00 (long)
    -> absorb middle into surrounding speaker
    """
    if len(segments) < 3:
        return segments

    smoothed = [segments[0]]

    i = 1
    while i < len(segments) - 1:
        prev_seg = smoothed[-1]
        curr_seg = segments[i]
        next_seg = segments[i + 1]

        curr_duration = curr_seg["end"] - curr_seg["start"]

        # A-B-A pattern with tiny middle segment
        if (
            prev_seg["speaker"] == next_seg["speaker"]
            and curr_seg["speaker"] != prev_seg["speaker"]
            and curr_duration < min_flip_duration
        ):
            # Merge into previous speaker
            prev_seg["end"] = next_seg["end"]
            i += 2  # skip next because merged
        else:
            smoothed.append(curr_seg)
            i += 1

    # append last segment if not already merged
    if smoothed[-1] != segments[-1]:
        smoothed.append(segments[-1])

    return smoothed