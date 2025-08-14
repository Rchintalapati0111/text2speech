# scrape.py
import trafilatura, fitz
from readability import Document
from bs4 import BeautifulSoup
import re

def extract_from_url(url: str) -> str:
    html = trafilatura.fetch_url(url)
    if not html: return ""
    text = trafilatura.extract(
        html, include_comments=False, include_tables=False, favor_recall=True
    )
    if not text:
        text = _fallback_readability(html)
    return _clean(text or "")

def _fallback_readability(html: str) -> str:
    doc = Document(html)
    soup = BeautifulSoup(doc.summary(), "html.parser")
    return soup.get_text(" ", strip=True)

def extract_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = " ".join(page.get_text("text") for page in doc)
    return _clean(text)

def _clean(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    # remove boilerplate that hurts TTS
    t = re.sub(r"©\s?\d{4}.*?$", "", t)
    return t
