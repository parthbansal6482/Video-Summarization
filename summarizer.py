from __future__ import annotations

import re
from typing import List

from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# spaCy + pyTextRank for TextRank-based extractive summarization
import spacy
import pytextrank  # noqa: F401  (needed to register the "textrank" pipeline component)


_NLP = None  # cached spaCy pipeline instance


def _get_nlp():
    """Load and cache spaCy model with pyTextRank pipeline.

    Attempts to load `en_core_web_sm`; if missing, downloads it.
    """
    global _NLP  # noqa: PLW0603 (module-level cache)
    if _NLP is not None:
        return _NLP

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Model not found; try to download at runtime
        from spacy.cli import download

        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    # Add textrank if not already present
    if "textrank" not in nlp.pipe_names:
        nlp.add_pipe("textrank")

    _NLP = nlp
    return _NLP


def _extract_video_id(youtube_url: str) -> str:
    """Extract YouTube video id from a variety of URL formats.

    Falls back to pytube.extract if direct parsing fails.
    """
    youtube_url = youtube_url.strip()
    # Common patterns: https://www.youtube.com/watch?v=VIDEOID, https://youtu.be/VIDEOID
    patterns = [
        r"(?:v=)([\w-]{11})",
        r"youtu\.be/([\w-]{11})",
        r"/shorts/([\w-]{11})",
    ]
    for pattern in patterns:
        found = re.search(pattern, youtube_url)
        if found:
            return found.group(1)
    # Fallback to pytube's extractor
    return extract.video_id(youtube_url)


def _fetch_transcript(video_id: str) -> List[str]:
    """Fetch transcript as a list of text chunks for the given video id using list_transcripts."""
    try:
        api = YouTubeTranscriptApi()
        transcripts = api.list(video_id)
        
        try:
            # Prefer native English
            items = transcripts.find_transcript(["en"]).fetch()
        except Exception:
            # Fallback: translate first available transcript to English
            try:
                first_available = next(iter(transcripts))
                items = first_available.translate("en").fetch()
            except Exception:
                return []
        
        return [i.text.strip() for i in items if i.text]
    except (TranscriptsDisabled, NoTranscriptFound):
        return []

                
def _split_into_sentences(text: str) -> List[str]:
    # Simple sentence splitter that handles periods, exclamation marks, and question marks.
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def _summarize_textrank(full_text: str, limit_phrases: int = 20, limit_sentences: int = 10) -> str:
    """Summarize using spaCy + pyTextRank (TextRank extractive summarization)."""
    nlp = _get_nlp()
    doc = nlp(full_text)
    sentences = [s.text for s in doc._.textrank.summary(limit_phrases=limit_phrases, limit_sentences=limit_sentences)]
    return " ".join(sentences).strip()


def summarize_youtube_video(youtube_url: str) -> str:
    """Return a concise summary for the given YouTube URL.

    Steps:
    1) Extract video id
    2) Fetch transcript
    3) Run a lightweight extractive summarizer
    """
    video_id = _extract_video_id(youtube_url)
    if not video_id:
        return ""

    chunks = _fetch_transcript(video_id)
    if not chunks:
        return ""

    full_text = " ".join(chunks)
    if not full_text.strip():
        return ""

    summary = _summarize_textrank(full_text, limit_phrases=20, limit_sentences=10)
    return summary


