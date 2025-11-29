"""Parser utilities for turning feed entries into structured records."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


@dataclass
class ArticleRecord:
    """Normalized representation of a news article."""

    title: str
    link: str
    published: datetime
    summary: str
    source: str
    raw: Dict[str, Any]


class ArticleParser:
    """Convert feedparser entries into ArticleRecord instances."""

    def parse_entry(self, entry: Any, source: str) -> Optional[ArticleRecord]:
        try:
            published_str = entry.get("published") or entry.get("updated")
            published = (
                date_parser.parse(published_str) if published_str else datetime.utcnow()
            )
            summary = entry.get("summary") or entry.get("description") or ""
            record = ArticleRecord(
                title=entry.get("title", "Untitled"),
                link=entry.get("link", ""),
                published=published,
                summary=summary,
                source=source,
                raw=dict(entry),
            )
            logger.debug("Parsed article '%s' from %s", record.title, source)
            return record
        except Exception as exc:  # noqa: BLE001 - log unexpected parsing issues
            logger.exception("Failed to parse entry from %s: %s", source, exc)
            return None
