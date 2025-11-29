"""Al Jazeera feed configuration."""
from aggregator.sources.base import BaseSource


class AlJazeeraSource(BaseSource):
    name = "Al Jazeera"
    feed_urls = [
        "https://www.aljazeera.com/xml/rss/all.xml",
    ]
