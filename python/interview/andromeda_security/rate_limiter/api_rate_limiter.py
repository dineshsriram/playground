from typing import NamedTuple
from .lookup_store import (
    DEFAULT_BURST_LIMIT_PER_SECOND,
    DEFAULT_LIMIT_PER_SECOND,
    DEFAULT_NUMBER_OF_BURST_PER_MINUTE,
    LookupStore,
    RateLimiterData,
)


class ApiData(NamedTuple):
    """
    Represents the metadata required to perform rate limiting for a specific API request.

    Attributes:
        api_key (str): The API key used to authenticate the client making the request.
        api_route (str): The normalized route or endpoint being accessed (e.g., '/user/:id').
        epoch_time (int): The Unix timestamp (in seconds) at which the request is made.
    """

    api_key: str
    api_route: str
    epoch_time: int


class RateLimiter:
    """
    Rate limiter implementation with per-second and burst limit checks.

    Features:
    - Per-second rate limiting
    - Burst limit tracking (allows bursts up to a threshold per minute)
    """

    def __init__(self):
        self.lookup_store = LookupStore()

    def increase_incoming_request_count(self, api_data: ApiData) -> None:
        self.lookup_store.increment_limit_count_by_one(
            api_data.api_key, api_data.api_route, api_data.epoch_time
        )

    def is_request_allowed(self, api_data: ApiData) -> bool:
        return self.is_request_under_per_second_limit(
            api_data
        ) or self.is_request_under_burstable_limit(api_data)

    def is_request_under_per_second_limit(self, api_data: ApiData) -> bool:
        data = self.lookup_store.get(api_data.api_key, api_data.api_route)
        current_count = data.api_counts_by_epoch_time.get(api_data.epoch_time, 0)
        return current_count <= DEFAULT_LIMIT_PER_SECOND

    def is_request_under_burstable_limit(self, api_data: ApiData) -> bool:
        """
        Check if the request is under the burst limit.

        A burst is defined as a second where the count exceeds the burst limit.
        We allow a certain number of bursts per minute.

        Args:
            api_data: The API request metadata
            lookup_data: The rate limiter data for this key/route

        Returns:
            True if under the burst limit, False otherwise
        """
        data = self.lookup_store.get(api_data.api_key, api_data.api_route)
        minute_ago = api_data.epoch_time - 60

        bursts_count = sum(
            1
            for epoch_time, count in data.api_counts_by_epoch_time.items()
            if minute_ago <= epoch_time <= api_data.epoch_time
            and count >= DEFAULT_BURST_LIMIT_PER_SECOND
        )

        return bursts_count <= DEFAULT_NUMBER_OF_BURST_PER_MINUTE
