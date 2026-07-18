# Digital Trends Agent

A modular pipeline that detects emerging fashion trends from public digital
signals, for retailers like Hammadi Abid to feed into demand forecasting
and procurement decisions.

```
Google Trends   Fashion News   YouTube
  Collector      Collector    Collector
      │             │             │
      ▼             ▼             ▼
              TrendSignal[]
                    │
                    ▼
            Trend Fusion Engine
                    │
                    ▼
              FusedTrend[]
                    │
                    ▼
          LLM Reasoner (Claude/Gemini)
                    │
                    ▼
              TrendReport (JSON)
```

Every collector is independent and returns the same `TrendSignal` shape
(`models.py`), so adding a new source later (Pinterest, TikTok Creative
Center, ...) means writing one new collector class - nothing else changes.

## Setup

```bash
pip install -r requirements.txt
```

Set an LLM key (used only for the news/YouTube extraction step and the
final narrative - everything else is deterministic arithmetic):

```bash
# pick ONE provider
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# or
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=...
```

If no key is set, the pipeline still runs and produces the fused JSON
data - only the narrative text is skipped. Good for demoing the pipeline
architecture without needing a key on hand.

## Run

```bash
# full pipeline, all 3 collectors, live network calls
python main.py

# only specific collectors
python main.py --sources google_trends fashion_news

# no network at all - runs fusion + reasoning on bundled sample signals
# (useful to demo/verify the fusion logic and LLM reasoning independently
# of whether Google Trends / YouTube / RSS are reachable right now)
python main.py --mock
```

Output is written to `trend_report.json` (change with `--out`).

## Module notes / things to check in your environment

- **Google Trends** (`collectors/google_trends_collector.py`): uses
  `pytrends`, an unofficial wrapper - no API key, but Google does
  rate-limit (HTTP 429) if you query too fast. `request_delay` between
  batches is already built in; raise it if you get blocked. The seed
  vocabulary lives in `config/fashion_vocabulary.json` - edit it to match
  your retailer's actual catalog. `geo="TN"` targets Tunisia specifically,
  but niche keywords can return all-zero data at country level; the code
  defaults to worldwide (`geo=""`) in the `__main__` block for that reason
  - switch back to `"TN"` once you've checked which keywords have local
  volume.
- **Fashion News** (`collectors/fashion_news_collector.py`): pulls from
  RSS feeds listed in `config/news_sources.json`. I could not verify
  these exact feed URLs are still live from this sandbox (no network
  access to fetch them here) - please confirm each URL resolves in your
  browser/environment before the demo, and swap in any that have moved.
- **YouTube** (`collectors/youtube_collector.py`): uses `yt-dlp`'s search
  extractor, no official API key needed. It's metadata-only (title +
  truncated description, no downloads), so it's fast, but YouTube can
  occasionally throttle repeated searches from the same IP - if that
  happens, add delays between queries similar to the Google Trends
  collector.
- **Fusion weights** (`fusion.py`): `SOURCE_WEIGHTS` gives Google Trends
  50% of the final score since it's the most reliable leading indicator,
  news/YouTube 25% each as corroboration. Tune these based on what you
  observe in your actual runs.

## Files

```
digital_trends_agent/
├── models.py                       # TrendSignal, FusedTrend, TrendReport
├── fusion.py                       # normalization + weighted scoring
├── reasoner.py                     # LLM narrative generation
├── llm_client.py                   # Claude/Gemini provider switch
├── main.py                         # orchestrator / CLI
├── config/
│   ├── fashion_vocabulary.json     # seed keywords for Google Trends
│   └── news_sources.json           # RSS feed list
├── collectors/
│   ├── base.py
│   ├── google_trends_collector.py
│   ├── fashion_news_collector.py
│   └── youtube_collector.py
└── tests/
    └── sample_signals.py           # mock data for --mock mode
```
