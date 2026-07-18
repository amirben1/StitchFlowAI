"""
Module 3 - YouTube Fashion Trend Collector.

Uses yt-dlp's search extractor (ytsearch:) to pull recent video titles +
descriptions for a set of fashion queries - no official YouTube Data API
key required, no per-video transcript downloads (keeps it fast and
demo-safe). Titles/descriptions are fed to the LLM for the same
structured extraction used by the news collector.
"""

import json
import os
import sys
from typing import List

import yt_dlp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import TrendSignal
from llm_client import complete
from .base import BaseCollector

DEFAULT_QUERIES = [
    "summer outfit ideas 2026",
    "streetwear haul",
    "fashion trends this season",
    "old money outfit",
    "men fashion trends",
    "women fashion trends",
]

EXTRACTION_SYSTEM_PROMPT = """You are a fashion trend analyst. You will be given a list of \
recent YouTube fashion video titles and descriptions. Extract the specific products, \
styles, colors, or materials being discussed as trending. Respond ONLY with valid JSON, \
no preamble, no markdown fences, in this exact schema:

{
  "mentions": [
    {"topic": "cargo pants", "mention_count": 4, "sentiment": "positive", "evidence": "short reason"}
  ]
}

If nothing fashion-relevant is found, return {"mentions": []}."""


class YouTubeCollector(BaseCollector):
    source_name = "youtube"

    def __init__(self, queries: List[str] = None, results_per_query: int = 8):
        self.queries = queries or DEFAULT_QUERIES
        self.results_per_query = results_per_query
        self.ydl_opts = {
            "quiet": True,
            "extract_flat": True,       # metadata only, no video download
            "skip_download": True,
            "no_warnings": True,
        }

    def _fetch_videos(self) -> List[dict]:
        videos = []
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            for q in self.queries:
                try:
                    search_key = f"ytsearch{self.results_per_query}:{q}"
                    result = ydl.extract_info(search_key, download=False)
                    for entry in result.get("entries", []):
                        videos.append({
                            "query": q,
                            "title": entry.get("title", ""),
                            "description": (entry.get("description") or "")[:200],
                        })
                except Exception as e:
                    print(f"[youtube] search failed for '{q}': {e}")
        return videos

    def collect(self) -> List[TrendSignal]:
        videos = self._fetch_videos()
        if not videos:
            return []

        digest = "\n".join(f"- {v['title']}: {v['description']}" for v in videos)
        user_prompt = f"Here are recent YouTube fashion video titles/descriptions:\n\n{digest}\n\nExtract trend mentions as JSON."

        raw = complete(EXTRACTION_SYSTEM_PROMPT, user_prompt)
        signals = []
        try:
            cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(cleaned)
            for m in parsed.get("mentions", []):
                count = m.get("mention_count", 1)
                sentiment = m.get("sentiment", "neutral")
                confidence = min(1.0, 0.25 + 0.1 * count)
                signals.append(TrendSignal(
                    source=self.source_name,
                    topic=m["topic"],
                    metric=float(count),
                    confidence=round(confidence, 2),
                    evidence=m.get("evidence", f"Mentioned in {count} videos, sentiment: {sentiment}"),
                    extra={"sentiment": sentiment, "video_count": len(videos)},
                ))
        except Exception as e:
            print(f"[youtube] could not parse LLM output: {e}\nRaw: {raw[:300]}")
        return signals


if __name__ == "__main__":
    for s in YouTubeCollector().collect():
        print(s.to_dict())
