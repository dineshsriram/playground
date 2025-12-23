from collections import UserDict, defaultdict
from typing import NamedTuple

DEFAULT_LIMIT_PER_SECOND = 10
DEFAULT_BURST_LIMIT_PER_SECOND = 100
DEFAULT_NUMBER_OF_BURST_PER_MINUTE = 2


class RateLimiterKey(NamedTuple):
    api_key: str
    api_route: str


class RateLimiterData:
    def __init__(self):
        self.limit_per_second = DEFAULT_LIMIT_PER_SECOND
        self.burst_limit_per_second = DEFAULT_BURST_LIMIT_PER_SECOND
        self.number_of_bursts = DEFAULT_NUMBER_OF_BURST_PER_MINUTE
        # This simulates the fixed window counter.
        # {100: 2, 101: 3, 102: 4}
        self.api_counts_by_epoch_time = defaultdict[int, int](int)


class LookupStore(UserDict[RateLimiterKey, RateLimiterData]):
    """
    This class simulates Redis KV Store. This is simply a dictionary for now so
    the focus is more on the implementation that we discussed.
    """

    def get(self, api_key: str, api_route: str) -> RateLimiterData:
        key = RateLimiterKey(api_key, api_route)
        return self.setdefault(key, RateLimiterData())

    def increment_limit_count_by_one(
        self, api_key: str, api_route: str, epoch_time: int
    ) -> None:
        # Key notes/assumptions:
        # 1. No locking here as I've assumed single threaded access
        # 2. Ignoring any serdes here for simplicity
        # 3. Updates need to be atomic and wrapped up in a transactional context if need be

        self.get(api_key, api_route).api_counts_by_epoch_time[epoch_time] += 1
