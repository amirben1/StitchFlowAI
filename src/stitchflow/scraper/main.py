"""
Digital Trends Agent - orchestrator.

Collectors -> Raw TrendSignals -> Fusion Engine -> FusedTrends -> LLM Reasoner -> TrendReport

Run:
    python main.py                       # all collectors
    python main.py --sources google_trends fashion_news
    python main.py --mock                # skip network calls, use bundled sample signals
"""

import argparse
import json
from datetime import datetime, timezone

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import TrendReport
from fusion import fuse
from reasoner import generate_narrative

COLLECTOR_REGISTRY = {}


def _lazy_import_collectors():
    """Import collectors lazily so --mock mode never needs pytrends/yt-dlp
    network calls to even import successfully."""
    from collectors.google_trends_collector import GoogleTrendsCollector
    from collectors.fashion_news_collector import FashionNewsCollector
    from collectors.youtube_collector import YouTubeCollector
    COLLECTOR_REGISTRY.update({
        "google_trends": GoogleTrendsCollector,
        "fashion_news": FashionNewsCollector,
        "youtube": YouTubeCollector,
    })


def run_pipeline(source_names=None, mock=False):
    if mock:
        from tests.sample_signals import SAMPLE_SIGNALS
        signals = SAMPLE_SIGNALS
    else:
        _lazy_import_collectors()
        active = source_names or list(COLLECTOR_REGISTRY.keys())
        signals = []
        for name in active:
            if name not in COLLECTOR_REGISTRY:
                print(f"[main] unknown source '{name}', skipping")
                continue
            print(f"[main] running collector: {name}")
            collector = COLLECTOR_REGISTRY[name]()
            collected = collector.collect()
            print(f"[main]   -> {len(collected)} signals")
            signals.extend(collected)

    print(f"[main] fusing {len(signals)} total signals...")
    fused = fuse(signals)

    print("[main] generating narrative...")
    narrative = generate_narrative(fused)

    report = TrendReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        fused_trends=fused,
        narrative=narrative,
    )
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digital Trends Agent")
    parser.add_argument("--sources", nargs="*", default=None,
                         help="subset of: google_trends fashion_news youtube")
    parser.add_argument("--mock", action="store_true",
                         help="use bundled sample signals instead of live network calls")
    parser.add_argument("--out", default="trend_report.json")
    args = parser.parse_args()

    report = run_pipeline(source_names=args.sources, mock=args.mock)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report.to_json())

    print(f"\n[main] report written to {args.out}\n")
    print(report.narrative)
