"""Bundled example signals, shaped exactly like what the real collectors
produce, so the fusion engine and reasoner can be exercised end-to-end
without hitting Google Trends / RSS / YouTube."""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import TrendSignal

SAMPLE_SIGNALS = [
    TrendSignal(source="google_trends", topic="linen shirt", metric=82, confidence=0.9,
                evidence="Search interest changed +38.0% over the period (latest index: 82/100).",
                extra={"growth_pct": 38.0}),
    TrendSignal(source="fashion_news", topic="linen shirt", metric=8, confidence=0.9,
                evidence="Multiple outlets cite linen as a leading summer fabric.",
                extra={"sentiment": "positive"}),
    TrendSignal(source="youtube", topic="linen shirt", metric=6, confidence=0.8,
                evidence="Linen shirts featured in several summer outfit videos.",
                extra={"sentiment": "positive"}),

    TrendSignal(source="google_trends", topic="cargo pants", metric=65, confidence=0.75,
                evidence="Search interest changed +12.0% over the period (latest index: 65/100).",
                extra={"growth_pct": 12.0}),
    TrendSignal(source="youtube", topic="cargo pants", metric=9, confidence=0.9,
                evidence="Cargo pants dominant in streetwear haul videos.",
                extra={"sentiment": "positive"}),

    TrendSignal(source="google_trends", topic="oversized hoodie", metric=20, confidence=0.4,
                evidence="Search interest changed -25.0% over the period (latest index: 20/100).",
                extra={"growth_pct": -25.0}),
    TrendSignal(source="fashion_news", topic="oversized hoodie", metric=1, confidence=0.4,
                evidence="Rarely mentioned in recent coverage.",
                extra={"sentiment": "neutral"}),

    TrendSignal(source="google_trends", topic="quiet luxury", metric=55, confidence=0.6,
                evidence="Search interest changed +5.0% over the period (latest index: 55/100).",
                extra={"growth_pct": 5.0}),
    TrendSignal(source="fashion_news", topic="quiet luxury", metric=5, confidence=0.6,
                evidence="Steady coverage as an ongoing aesthetic, not a spike.",
                extra={"sentiment": "positive"}),
]
