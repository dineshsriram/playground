from collections import UserDict, defaultdict
from typing import NamedTuple


DEFAULT_AVG_LIMIT_PER_SECOND = 10
DEFAULT_BURST_LIMIT_PER_MINUTE = 100


class RateLimiterKey(NamedTuple):
    api_key: str
    api_route: str


class RateLimiterData:
    def __init__(self):
        self.avg_limit_per_second = DEFAULT_AVG_LIMIT_PER_SECOND
        self.burst_limit_per_minute = DEFAULT_BURST_LIMIT_PER_MINUTE
        self.api_counts_by_timestamp = defaultdict[int, int](int)


class LookupStore(UserDict):
    """
    This class simulates Redis KV Store. This is simply a dictionary for now so
    the focus is more on the implementation that we discussed.

    In production, the updates need to be atomic and wrapped up in a transactional context if need be,
    serdes etc.
    """
