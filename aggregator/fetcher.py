"""Utilities for fetching news stories from configured sources."""
from __future__ import annotations

import logging
from typing import Dict, Iterable, List, Type

from aggregator.parser import ArticleRecord
from aggregator.sources.aljazeera import AlJazeeraSource
from aggregator.sources.bbc import BBCSource
from aggregator.sources.base import BaseSource
from aggregator.sources.guardian import GuardianSource
from aggregator.sources.npr import NPRSource
from aggregator.sources.reuters import ReutersSource

logger = logging.getLogger(__name__)


class NewsFetcher:
    """Coordinates pulling articles from all configured sources."""

    SOURCE_MAP: Dict[str, Type[BaseSource]] = {
        "reuters": ReutersSource,
        "bbc": BBCSource,
        "npr": NPRSource,
        "guardian": GuardianSource,
        "aljazeera": AlJazeeraSource,
    }

    def __init__(self, enabled_sources: Iterable[str] | None = None) -> None:
        self.enabled_sources = (
            set(enabled_sources) if enabled_sources else set(self.SOURCE_MAP.keys())
        )

    def fetch_all(self) -> List[ArticleRecord]:
        """Pull articles from every enabled source."""
        articles: List[ArticleRecord] = []
        for key in self.enabled_sources:
            source_cls = self.SOURCE_MAP.get(key)
            if not source_cls:
                logger.warning("Source %s is not recognized; skipping", key)
                continue
            source = source_cls()
            logger.info("Fetching articles from %s", source.name)
            articles.extend(source.fetch())
        return articles
