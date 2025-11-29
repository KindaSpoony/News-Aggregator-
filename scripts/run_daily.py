"""Entry point for the Nightwalker daily aggregation pipeline."""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from aggregator import NewsFetcher, NightwalkerAnalyzer, ReportBuilder

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_config(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main(config_path: str = "config.yaml") -> None:
    config = load_config(config_path)
    enabled_sources = [
        key for key, value in config.get("sources", {}).items() if value.get("enabled", True)
    ]

    fetcher = NewsFetcher(enabled_sources=enabled_sources)
    analyzer = NightwalkerAnalyzer(ri_depth=config.get("ri_depth", 16), model=config.get("model", "gpt-5.1"))
    report_builder = ReportBuilder(output_dir=config.get("output_dir", "reports"), gpt_client=analyzer.gpt)

    logger.info("Starting daily news aggregation for sources: %s", ", ".join(enabled_sources))
    articles = fetcher.fetch_all()
    analyses = analyzer.analyze_records(articles)
    report_path = report_builder.build(analyses)
    logger.info("Daily report available at %s", report_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Daily run failed: %s", exc)
        sys.exit(1)
