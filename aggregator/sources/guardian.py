"""The Guardian feed configuration."""
from aggregator.sources.base import BaseSource


class GuardianSource(BaseSource):
    name = "The Guardian"
    feed_urls = [
        "https://www.theguardian.com/world/rss",
        "https://www.theguardian.com/international/rss",
    ]
