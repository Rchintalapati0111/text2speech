# tts_engine.py
from pathlib import Path
from functools import lru_cache
from typing import Optional
from TTS.api import TTS
import re
from pydub import AudioSegment, effects
import math
import tempfile

# default model (good naturalness); add more if you like
DEFAULT_MODEL = "tts_models/en/ljspeech/tacotron2-DDC_ph"
ALT_MODEL = "tts_models/en/vctk/vits"  # multi-speaker (downloads on first use)

@lru_cache(maxsize=4)
def _get_tts(model_name: str, use_gpu: bool = False):
    return TTS(model_name, progress_bar=False, gpu=use_gpu)

def synthesize_text(text, out_path, model_name=DEFAULT_MODEL, speed=1.0, use_gpu=False):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    # Fresh model instance per call avoids Tacotron2 attention carry-over
    tts = TTS(model_name, progress_bar=False, gpu=use_gpu)

    text = re.sub(r"\s+", " ", text).strip()
    chunks = _chunk_text(text, max_len=350)  # shorter chunks keep Tacotron2 happy
    pieces = []
    for ch in chunks:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            # IMPORTANT: don't let the API split again
            tts.tts_to_file(text=ch, file_path=tmp.name, split_sentences=False)
            pieces.append(AudioSegment.from_file(tmp.name))

    audio = _concat_with_silence(pieces, silence_ms=250)
    if abs(speed - 1.0) > 1e-3:
        audio = effects.speedup(audio, playback_speed=speed, crossfade=50)
    audio.export(out_path, format="wav")
    return out_path

def _chunk_text(text: str, max_len: int = 1200):
    # split on sentence boundaries, fall back to hard wraps
    import re
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, cur = [], ""
    for s in sents:
        if len(cur) + len(s) + 1 <= max_len:
            cur = f"{cur} {s}".strip()
        else:
            if cur: chunks.append(cur)
            if len(s) <= max_len:
                cur = s
            else:
                # hard wrap long sentence
                for i in range(0, len(s), max_len):
                    chunks.append(s[i:i+max_len])
                cur = ""
    if cur: chunks.append(cur)
    return [c.strip() for c in chunks if c.strip()]

def _concat_with_silence(segments, silence_ms=250):
    if not segments: return AudioSegment.silent(duration=1)
    silence = AudioSegment.silent(duration=silence_ms)
    audio = segments[0]
    for seg in segments[1:]:
        audio += silence + seg
    return audio
