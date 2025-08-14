# app.py
import streamlit as st
from pathlib import Path
from scrape import extract_from_url, extract_from_pdf
from normalize import normalize_text
from tts_engine import synthesize_text, DEFAULT_MODEL, ALT_MODEL

st.set_page_config(page_title="Accessible TTS", layout="wide")
st.title("Accessible Web/PDF → Speech")

# Controls
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("Voice/Model", [DEFAULT_MODEL, ALT_MODEL], index=0)
    speed = st.slider("Playback speed", 0.7, 1.5, 1.0, 0.05)
    st.caption("Tip: 0.9–1.2 stays natural. Extreme values may sound artifact-y.")

tab1, tab2 = st.tabs(["From URL", "From PDF"])

with tab1:
    url = st.text_input("Web page URL", placeholder="https://example.com/article")
    if st.button("Convert URL") and url:
        with st.status("Fetching & normalizing text…", expanded=False):
            raw = extract_from_url(url)
            text = normalize_text(raw)
        st.write(f"Characters: {len(text)}")
        if not text:
            st.error("No extractable content found.")
        else:
            out_path = "out/url_tts.wav"
            with st.status("Synthesizing audio… this may take a moment", expanded=False):
                synthesize_text(text, out_path, model_name=model_name, speed=speed)
            st.success("Done!")
            st.audio(out_path)
            st.download_button("Download WAV", open(out_path, "rb"), file_name="tts.wav")

with tab2:
    up = st.file_uploader("Upload PDF", type=["pdf"])
    if up and st.button("Convert PDF"):
        tmp = Path("out") / up.name
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_bytes(up.read())
        with st.status("Reading & normalizing PDF…", expanded=False):
            raw = extract_from_pdf(str(tmp))
            text = normalize_text(raw)
        st.write(f"Characters: {len(text)}")
        if not text:
            st.error("No text found in PDF.")
        else:
            out_path = "out/pdf_tts.wav"
            with st.status("Synthesizing audio…", expanded=False):
                synthesize_text(text, out_path, model_name=model_name, speed=speed)
            st.success("Done!")
            st.audio(out_path)
            st.download_button("Download WAV", open(out_path, "rb"), file_name="pdf_tts.wav")

st.caption("Keyboard: Tab to focus, Enter to activate.")
