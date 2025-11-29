"""Reuters feed configuration."""
from aggregator.sources.base import BaseSource


class ReutersSource(BaseSource):
    name = "Reuters"
    feed_urls = [
        "http://feeds.reuters.com/reuters/topNews",
        "http://feeds.reuters.com/reuters/worldNews",
    ]
