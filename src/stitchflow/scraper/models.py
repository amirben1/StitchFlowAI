"""
Common data models for the Digital Trends Agent.

Every collector (Google Trends, Fashion News, YouTube, ...) must emit
TrendSignal objects. This is the contract that keeps the Fusion Engine
and the Reasoning layer independent of *where* the data came from.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
import json


@dataclass
class TrendSignal:
    """A single piece of evidence about a topic, from a single source."""

    source: str            # e.g. "google_trends", "fashion_news", "youtube"
    topic: str              # normalized product/style name, e.g. "linen shirt"
    metric: float            # raw signal strength, source-specific scale
    confidence: float        # 0.0 - 1.0, how much to trust this signal
    evidence: str             # short human-readable justification
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    extra: Optional[dict] = None  # any source-specific extra data

    def to_dict(self) -> dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class FusedTrend:
    """Output of the Fusion Engine: one topic, combined across sources."""

    topic: str
    trend_score: float          # 0-100 normalized score
    confidence: float            # 0.0 - 1.0
    direction: str                 # "rising" | "declining" | "stable"
    contributing_sources: list       # list[str]
    evidence: list                    # list[str], one per contributing source

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TrendReport:
    """Final structured output of the whole pipeline, ready for the UI/API."""

    generated_at: str
    fused_trends: list        # list[FusedTrend]
    narrative: Optional[str] = None   # filled in by the LLM reasoning step

    def to_json(self, indent=2) -> str:
        payload = {
            "generated_at": self.generated_at,
            "narrative": self.narrative,
            "fused_trends": [t.to_dict() if isinstance(t, FusedTrend) else t
                              for t in self.fused_trends],
        }
        return json.dumps(payload, indent=indent, ensure_ascii=False)
