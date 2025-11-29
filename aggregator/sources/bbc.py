"""BBC feed configuration."""
from aggregator.sources.base import BaseSource


class BBCSource(BaseSource):
    name = "BBC"
    feed_urls = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
    ]
