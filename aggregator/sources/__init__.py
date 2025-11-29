"""Source configurations for supported news providers."""
from aggregator.sources.aljazeera import AlJazeeraSource
from aggregator.sources.bbc import BBCSource
from aggregator.sources.guardian import GuardianSource
from aggregator.sources.npr import NPRSource
from aggregator.sources.reuters import ReutersSource
from aggregator.sources.base import BaseSource

__all__ = [
    "AlJazeeraSource",
    "BBCSource",
    "GuardianSource",
    "NPRSource",
    "ReutersSource",
    "BaseSource",
]
