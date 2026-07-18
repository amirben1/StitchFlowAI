"""
Trend Fusion Engine.

Takes TrendSignal objects from every collector, groups them by topic,
normalizes each source's metric onto a common 0-100 scale, and combines
them into a single FusedTrend with a confidence-weighted score.

This is deliberately plain arithmetic, not an LLM call - the LLM should
reason over already-trustworthy numbers, not invent them.
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import List

from models import TrendSignal, FusedTrend

# How much each source counts toward the final score. Google Trends is
# the most reliable leading indicator of consumer intent, so it gets the
# most weight; news/YouTube mentions are corroborating evidence.
SOURCE_WEIGHTS = {
    "google_trends": 0.5,
    "fashion_news": 0.25,
    "youtube": 0.25,
}

# Rough normalization caps per source, so a "5 mentions in news" and a
# "82/100 Google Trends index" land on a comparable 0-100 scale.
NORMALIZATION_CAP = {
    "google_trends": 100.0,   # already 0-100
    "fashion_news": 10.0,     # ~10 mentions = saturated signal
    "youtube": 10.0,
}


def _normalize(source: str, metric: float) -> float:
    cap = NORMALIZATION_CAP.get(source, 100.0)
    return round(min(100.0, (metric / cap) * 100), 1)


def _topic_key(topic: str) -> str:
    return topic.strip().lower()


def fuse(signals: List[TrendSignal]) -> List[FusedTrend]:
    grouped = defaultdict(list)
    for s in signals:
        grouped[_topic_key(s.topic)].append(s)

    fused_trends = []
    for topic, sigs in grouped.items():
        weighted_sum = 0.0
        weight_total = 0.0
        confidences = []
        sources = []
        evidences = []
        growths = []

        for s in sigs:
            weight = SOURCE_WEIGHTS.get(s.source, 0.1) * s.confidence
            norm_score = _normalize(s.source, s.metric)
            weighted_sum += norm_score * weight
            weight_total += weight
            confidences.append(s.confidence)
            sources.append(s.source)
            evidences.append(f"[{s.source}] {s.evidence}")
            if s.extra and "growth_pct" in s.extra:
                growths.append(s.extra["growth_pct"])

        score = round(weighted_sum / weight_total, 1) if weight_total > 0 else 0.0
        avg_confidence = round(sum(confidences) / len(confidences), 2)

        # More sources agreeing => higher confidence, capped at 1.0
        agreement_bonus = min(0.15, 0.05 * (len(set(sources)) - 1))
        final_confidence = round(min(1.0, avg_confidence + agreement_bonus), 2)

        avg_growth = sum(growths) / len(growths) if growths else 0
        if avg_growth > 10 or (not growths and score > 60):
            direction = "rising"
        elif avg_growth < -10:
            direction = "declining"
        else:
            direction = "stable"

        # Use the original-cased topic from the first signal for display
        display_topic = sigs[0].topic

        fused_trends.append(FusedTrend(
            topic=display_topic,
            trend_score=score,
            confidence=final_confidence,
            direction=direction,
            contributing_sources=sorted(set(sources)),
            evidence=evidences,
        ))

    fused_trends.sort(key=lambda t: t.trend_score, reverse=True)
    return fused_trends
