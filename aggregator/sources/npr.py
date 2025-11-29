"""NPR feed configuration."""
from aggregator.sources.base import BaseSource


class NPRSource(BaseSource):
    name = "NPR"
    feed_urls = [
        "https://feeds.npr.org/1001/rss.xml",
        "https://feeds.npr.org/1004/rss.xml",
    ]
