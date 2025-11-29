# Nightwalker News Aggregator

Nightwalker News Aggregator collects stories from leading outlets, enriches them with Nightwalker Stack analysis, and produces a daily markdown report. The stack combines empirical, logical, emotional, and historical vectors with a four-agent overlay (Thinker, Doer, Controller, Pulse) to surface narrative drift, threat vectors, and source comparisons.

## Features
- RSS ingestion for Reuters, BBC, NPR, The Guardian, and Al Jazeera
- Article parsing into structured records with timestamps and summaries
- Nightwalker analysis vectors plus four-agent overlay
- Optional GPT-5 powered summarization, recursive insight (RI-16) passes, and report writing
- Daily report generation under `reports/YYYY-MM-DD-nightwalker-daily.md`

## Installation
1. Ensure Python 3.10+ is installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key if you want GPT-assisted analysis:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## Configuration
Adjust `config.yaml` to tune sources, concurrency, and output paths. Defaults are provided for the five supported sources and the daily report location under `reports/`.

## Usage
Run the daily pipeline from the project root:
```bash
python scripts/run_daily.py
```
The script fetches articles, parses and analyzes them, and writes the markdown report to the `reports/` directory. Logging output provides visibility into each step.

## Project Structure
- `aggregator/fetcher.py` – orchestrates pulling articles from each source
- `aggregator/parser.py` – normalizes feed entries into structured article records
- `aggregator/analyzer.py` – Nightwalker stack analysis and GPT-assisted insight
- `aggregator/report_builder.py` – composes the markdown daily report
- `aggregator/sources/` – source-specific feed configurations
- `scripts/run_daily.py` – end-to-end driver for the daily workflow
