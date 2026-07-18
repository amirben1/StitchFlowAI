"""
Module 2 - Fashion News Collector.

Pulls recent articles from a curated list of RSS feeds, then asks the
LLM to extract structured trend mentions (product / color / material /
style + sentiment) from the headlines+summaries. No scraping of full
article bodies required - RSS summaries are usually enough signal.
"""

import json
import os
import sys
from typing import List

import feedparser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import TrendSignal
from llm_client import complete
from .base import BaseCollector

SOURCES_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "news_sources.json")

EXTRACTION_SYSTEM_PROMPT = """You are a fashion trend analyst. You will be given a list of \
recent fashion news headlines and summaries. Extract the specific products, styles, \
colors, or materials being discussed as trending. Respond ONLY with valid JSON, no \
preamble, no markdown fences, in this exact schema:

{
  "mentions": [
    {"topic": "linen shirt", "mention_count": 3, "sentiment": "positive", "evidence": "short reason"}
  ]
}

If nothing fashion-relevant is found, return {"mentions": []}."""


class FashionNewsCollector(BaseCollector):
    source_name = "fashion_news"

    def __init__(self, sources_path: str = SOURCES_PATH, max_articles_per_feed: int = 15):
        with open(sources_path, "r", encoding="utf-8") as f:
            self.sources = json.load(f)["sources"]
        self.max_articles_per_feed = max_articles_per_feed

    def _fetch_articles(self) -> List[dict]:
        articles = []
        for src in self.sources:
            try:
                feed = feedparser.parse(src["rss"])
                for entry in feed.entries[: self.max_articles_per_feed]:
                    articles.append({
                        "source": src["name"],
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", entry.get("description", "")),
                    })
            except Exception as e:
                print(f"[fashion_news] failed to fetch {src['name']}: {e}")
        return articles

    def collect(self) -> List[TrendSignal]:
        articles = self._fetch_articles()
        if not articles:
            return []

        digest = "\n".join(
            f"- ({a['source']}) {a['title']}: {a['summary'][:200]}" for a in articles
        )
        user_prompt = f"Here are recent fashion news items:\n\n{digest}\n\nExtract trend mentions as JSON."

        raw = complete(EXTRACTION_SYSTEM_PROMPT, user_prompt)
        signals = []
        try:
            cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(cleaned)
            for m in parsed.get("mentions", []):
                count = m.get("mention_count", 1)
                sentiment = m.get("sentiment", "neutral")
                confidence = min(1.0, 0.3 + 0.1 * count)
                signals.append(TrendSignal(
                    source=self.source_name,
                    topic=m["topic"],
                    metric=float(count),
                    confidence=round(confidence, 2),
                    evidence=m.get("evidence", f"Mentioned {count}x, sentiment: {sentiment}"),
                    extra={"sentiment": sentiment, "article_count": len(articles)},
                ))
        except Exception as e:
            print(f"[fashion_news] could not parse LLM output: {e}\nRaw: {raw[:300]}")
        return signals


if __name__ == "__main__":
    for s in FashionNewsCollector().collect():
        print(s.to_dict())
