Accessible Web/PDF → Speech (TTS)  
Turn any web page or PDF into clear, natural speech.
Built with Streamlit, robust content extraction, light text normalization, and Coqui TTS (Tacotron2 + UnivNet). Optional Piper backend for fast, offline CPU synthesis.

✨ Features
URL → audio and PDF → audio

Clean extraction with trafilatura (fallback to Readability)

Lightweight normalization (abbreviations, numbers → words)

Chunked synthesis for stable long-form reading

Playback speed control (0.7–1.5×)

Keyboard-first UI, high-contrast friendly

Saves output WAV to out/ + download button

Optional multi-speaker model (VCTK VITS)

Optional offline synthesis with Piper

📂 Project structure
```
TTS/
  app.py
  scrape.py
  normalize.py
  tts_engine.py
  requirements.txt
  out/                # generated audio (gitignored)
  .venv/              # local venv (gitignored)
```
🧰 Prerequisites
1. Python 3.10+ recommended (3.9 works but may need a small pin; see Troubleshooting)

2. macOS/Linux/Windows

3. ffmpeg (for pydub time-stretch):

4. macOS: brew install ffmpeg


🚀 Quickstart
```
# clone your repo
git clone https://github.com/Rchintalapati0111/text2speech.git
cd text2speech

# create & activate venv
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# upgrade tooling
python -m pip install -U pip setuptools wheel

# install deps
pip install -r requirements.txt

# run (use the venv interpreter so it sees installed packages)
python -m streamlit run app.py
```
Open the URL Streamlit prints (default: http://localhost:8501).

🧠 How it works (pipeline)
```
URL/PDF  ──►  scrape.py  ──►  normalize.py  ──►  tts_engine.py  ──►  WAV
                 ↑                    ↑              ↑
         trafilatura/Readability   abbrev & #s    Coqui TTS (Tacotron2→mel)
                                                   + UnivNet vocoder
```
1. Scraping: trafilatura extracts the main content. If it can’t, we fall back to Readability.

2. Normalization: expands abbreviations (e.g. → for example), converts short numbers to words.

3. Synthesis:

Default: Tacotron2 predicts mel-spectrogram → UnivNet vocoder → waveform.

We chunk long text (sentence-aware) and add 250ms pauses between chunks for natural pacing.

Speed slider applies a safe time-stretch.

⚙️ Configuration
Edit tts_engine.py to change voices/models:

```
DEFAULT_MODEL = "tts_models/en/ljspeech/tacotron2-DDC_ph"  # single speaker, natural
ALT_MODEL     = "tts_models/en/vctk/vits"                  # multi-speaker (downloads on first use)
```
In app.py, the sidebar lets you pick between DEFAULT_MODEL and ALT_MODEL, and adjust speed.

🧩 Files overview
A. app.py
Streamlit UI:

Tab 1: enter URL → fetch, normalize → synthesize → play/download

Tab 2: upload PDF → read with PyMuPDF → normalize → synthesize → play/download

B. scrape.py
extract_from_url(url): trafilatura → fallback to Readability → clean whitespace/boilerplate

extract_from_pdf(path): PyMuPDF (fitz) text extraction → clean

C. normalize.py
Expands common abbreviations (Mr., Dr., etc.), weekdays/months, Latinisms (e.g., i.e.)

Converts short integers to words via num2words

Collapses excessive whitespace

D. tts_engine.py
Loads model, splits text to chunks, synthesizes each piece, joins with short silences

Optional post-process speed change with pydub.effects.speedup

🖱️ Using the app
1. From URL

Paste a readable article link.

Click Convert URL → audio appears with a download button.

2. From PDF

Upload a text-based PDF (not a scanned image).

3. Click Convert PDF → audio appears with a download button.

Adjust speed in the sidebar (0.7–1.5×).

4. Select Voice/Model in the sidebar.

