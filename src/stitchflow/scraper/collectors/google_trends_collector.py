"""
Module 1 - Google Trends Collector.

Google Trends has no "what's trending in fashion right now" endpoint - it
only answers "how popular is THIS keyword". So we feed it a seed
vocabulary (config/fashion_vocabulary.json) and rank by recent growth.
This mirrors how real retail trend-analytics tools work.
"""

import json
import os
import time
from datetime import datetime, timezone
from typing import List

from pytrends.request import TrendReq

from .base import BaseCollector
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import TrendSignal

VOCAB_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "fashion_vocabulary.json")


class GoogleTrendsCollector(BaseCollector):
    source_name = "google_trends"

    def __init__(self, geo: str = "TN", timeframe: str = "today 3-m",
                 vocab_path: str = VOCAB_PATH, request_delay: float = 1.0):
        """
        geo: country code for localized interest (e.g. "TN" for Tunisia,
             "" for worldwide). Tunisia-specific data can be sparse for
             niche keywords - fall back to "" if you get too many zeros.
        timeframe: pytrends timeframe string, "today 3-m" = last 3 months.
        request_delay: seconds to sleep between keyword batches, to avoid
             Google Trends rate-limiting (HTTP 429).
        """
        self.geo = geo
        self.timeframe = timeframe
        self.request_delay = request_delay
        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab = json.load(f)
        self.keywords = [kw for group in vocab.values() for kw in group]
        self.pytrends = TrendReq(hl="en-US", tz=0)

    @staticmethod
    def _growth_rate(series) -> float:
        """% change between the average of the first half and second half
        of the series - more stable than a single first-vs-last point."""
        n = len(series)
        if n < 4:
            return 0.0
        mid = n // 2
        first_half_avg = sum(series[:mid]) / mid
        second_half_avg = sum(series[mid:]) / (n - mid)
        if first_half_avg == 0:
            return 100.0 if second_half_avg > 0 else 0.0
        return round(((second_half_avg - first_half_avg) / first_half_avg) * 100, 1)

    def _fetch_batch(self, keywords_batch: List[str]) -> List[TrendSignal]:
        signals = []
        try:
            self.pytrends.build_payload(keywords_batch, timeframe=self.timeframe, geo=self.geo)
            df = self.pytrends.interest_over_time()
        except Exception as e:
            print(f"[google_trends] batch failed {keywords_batch}: {e}")
            return signals

        if df is None or df.empty:
            return signals

        for kw in keywords_batch:
            if kw not in df.columns:
                continue
            series = df[kw].tolist()
            latest = series[-1] if series else 0
            growth = self._growth_rate(series)
            # confidence scales with average interest level - a "trend"
            # built on near-zero search volume is unreliable
            avg_interest = sum(series) / len(series) if series else 0
            confidence = min(1.0, max(0.1, avg_interest / 60))
            signals.append(TrendSignal(
                source=self.source_name,
                topic=kw,
                metric=float(latest),
                confidence=round(confidence, 2),
                evidence=f"Search interest changed {growth:+.1f}% over the period "
                         f"(latest index: {latest}/100).",
                extra={"growth_pct": growth, "series": series, "geo": self.geo},
            ))
        return signals

    def collect(self) -> List[TrendSignal]:
        signals: List[TrendSignal] = []
        # pytrends allows max 5 keywords per request
        for i in range(0, len(self.keywords), 5):
            batch = self.keywords[i:i + 5]
            signals.extend(self._fetch_batch(batch))
            time.sleep(self.request_delay)
        return signals


if __name__ == "__main__":
    collector = GoogleTrendsCollector(geo="")  # worldwide, more data density
    for s in collector.collect():
        print(s.to_dict())
