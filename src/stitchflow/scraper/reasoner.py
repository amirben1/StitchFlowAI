"""
Reasoning layer. Takes the already-fused, already-trustworthy trend
data and asks the LLM to write the executive narrative - it never sees
raw articles/searches, only clean numbers, so it can't hallucinate
evidence that isn't there.
"""

import json
from typing import List

from models import FusedTrend
from llm_client import complete

SYSTEM_PROMPT = """You are a Fashion Trend Analyst producing a report for a clothing \
retailer's merchandising and procurement team. You will receive structured, \
pre-computed trend scores (0-100) with confidence levels and source evidence. \
Do not invent any data not present in the input. Write a concise, decision-ready \
report with these sections:

1. Executive Summary (2-3 sentences)
2. Emerging Trends (rising, high-confidence topics)
3. Declining Trends (if any)
4. Procurement Implications (concrete, e.g. "increase X% stock of...")

Keep it under 350 words. Plain text, no markdown headers needed beyond simple labels."""


def generate_narrative(fused_trends: List[FusedTrend]) -> str:
    payload = [t.to_dict() for t in fused_trends]
    user_prompt = f"Fused trend data:\n\n{json.dumps(payload, indent=2)}\n\nWrite the report."
    return complete(SYSTEM_PROMPT, user_prompt, max_tokens=800)
