"""Shared source utilities."""
from __future__ import annotations

import logging
from typing import Iterable, List

import feedparser

from aggregator.parser import ArticleParser, ArticleRecord

logger = logging.getLogger(__name__)


class BaseSource:
    """Represents a news source that exposes one or more feeds."""

    name: str
    feed_urls: Iterable[str]

    def fetch(self) -> List[ArticleRecord]:
        """Fetch and parse feeds into article records."""
        parser = ArticleParser()
        articles: List[ArticleRecord] = []
        for url in self.feed_urls:
            logger.debug("Fetching feed for %s from %s", self.name, url)
            feed = feedparser.parse(url)
            for entry in feed.entries:
                record = parser.parse_entry(entry, source=self.name)
                if record:
                    articles.append(record)
        logger.info("Fetched %d articles from %s", len(articles), self.name)
        return articles
