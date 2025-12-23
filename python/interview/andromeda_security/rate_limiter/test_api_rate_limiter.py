import pytest
from .api_rate_limiter import RateLimiter, ApiData
from .lookup_store import (
    DEFAULT_LIMIT_PER_SECOND,
    DEFAULT_BURST_LIMIT_PER_SECOND,
    DEFAULT_NUMBER_OF_BURST_PER_MINUTE,
)


class TestRateLimiter:
    @pytest.fixture
    def rate_limiter(self):
        """Create a fresh RateLimiter instance for each test."""
        return RateLimiter()

    @pytest.fixture
    def base_epoch_time(self):
        """Base epoch time for tests."""
        return 1000

    def test_is_request_allowed_when_no_requests(self, rate_limiter, base_epoch_time):
        """Test that requests are allowed when no previous requests exist."""
        api_data = ApiData(
            api_key="test_key", api_route="/test", epoch_time=base_epoch_time
        )
        assert rate_limiter.is_request_allowed(api_data) is True

    def test_burst_limit_enforcement(self, rate_limiter, base_epoch_time):
        """Test that burst limit is enforced per minute."""
        api_key = "test_key"
        api_route = "/test"
        start_epoch = base_epoch_time

        # Create bursts up to the allowed limit
        for burst_num in range(DEFAULT_NUMBER_OF_BURST_PER_MINUTE):
            epoch_time = start_epoch + burst_num
            # Create a burst (exceed DEFAULT_BURST_LIMIT_PER_SECOND)
            for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
                api_data = ApiData(
                    api_key=api_key, api_route=api_route, epoch_time=epoch_time
                )
                rate_limiter.increase_incoming_request_count(api_data)

        # Create one more burst - should still be allowed (we're at the limit)
        new_epoch = start_epoch + DEFAULT_NUMBER_OF_BURST_PER_MINUTE
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=new_epoch)
        # First request in this burst should be allowed
        assert rate_limiter.is_request_allowed(api_data) is True

        # Create the burst
        for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
            api_data = ApiData(
                api_key=api_key, api_route=api_route, epoch_time=new_epoch
            )
            rate_limiter.increase_incoming_request_count(api_data)

        # Now we've exceeded the burst limit per minute
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=new_epoch)
        assert rate_limiter.is_request_allowed(api_data) is False

    def test_burst_limit_window_is_one_minute(self, rate_limiter, base_epoch_time):
        """Test that burst limit window is exactly one minute (60 seconds)."""
        api_key = "test_key"
        api_route = "/test"
        start_epoch = base_epoch_time

        # Create bursts at the limit
        for burst_num in range(DEFAULT_NUMBER_OF_BURST_PER_MINUTE):
            epoch_time = start_epoch + burst_num
            for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
                api_data = ApiData(
                    api_key=api_key, api_route=api_route, epoch_time=epoch_time
                )
                rate_limiter.increase_incoming_request_count(api_data)

        # Create another burst - should exceed limit
        new_epoch = start_epoch + DEFAULT_NUMBER_OF_BURST_PER_MINUTE
        for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
            api_data = ApiData(
                api_key=api_key, api_route=api_route, epoch_time=new_epoch
            )
            rate_limiter.increase_incoming_request_count(api_data)

        # Should be blocked
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=new_epoch)
        assert rate_limiter.is_request_allowed(api_data) is False

        # But if we wait 61 seconds, the first burst should be out of window
        old_burst_epoch = start_epoch + 61
        api_data = ApiData(
            api_key=api_key, api_route=api_route, epoch_time=old_burst_epoch
        )
        # Should be allowed again (first burst is now out of the 60-second window)
        assert rate_limiter.is_request_allowed(api_data) is True

    def test_is_request_under_per_second_limit(self, rate_limiter, base_epoch_time):
        """Test the per-second limit check method directly."""
        api_key = "test_key"
        api_route = "/test"
        epoch_time = base_epoch_time

        # Initially should be under limit
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=epoch_time)
        assert rate_limiter.is_request_under_per_second_limit(api_data) is True

        # At the limit should still be under
        for i in range(DEFAULT_LIMIT_PER_SECOND):
            rate_limiter.increase_incoming_request_count(api_data)
        assert rate_limiter.is_request_under_per_second_limit(api_data) is True

        # Over the limit
        rate_limiter.increase_incoming_request_count(api_data)
        assert rate_limiter.is_request_under_per_second_limit(api_data) is False

    def test_is_request_under_burstable_limit(self, rate_limiter, base_epoch_time):
        """Test the burst limit check method directly."""
        api_key = "test_key"
        api_route = "/test"
        start_epoch = base_epoch_time

        # Initially should be under burst limit
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=start_epoch)
        assert rate_limiter.is_request_under_burstable_limit(api_data) is True

        # Create bursts up to the limit
        for burst_num in range(DEFAULT_NUMBER_OF_BURST_PER_MINUTE):
            epoch_time = start_epoch + burst_num
            for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
                api_data = ApiData(
                    api_key=api_key, api_route=api_route, epoch_time=epoch_time
                )
                rate_limiter.increase_incoming_request_count(api_data)

        # Should still be under limit (at the limit)
        new_epoch = start_epoch + DEFAULT_NUMBER_OF_BURST_PER_MINUTE + 1
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=new_epoch)
        assert rate_limiter.is_request_under_burstable_limit(api_data) is True

        # Create one more burst
        for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
            api_data = ApiData(
                api_key=api_key, api_route=api_route, epoch_time=new_epoch
            )
            rate_limiter.increase_incoming_request_count(api_data)

        # Now should exceed burst limit
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=new_epoch)
        assert rate_limiter.is_request_under_burstable_limit(api_data) is False

    def test_combined_per_second_and_burst_limits(self, rate_limiter, base_epoch_time):
        """Test the interaction between per-second and burst limits."""
        api_key = "test_key"
        api_route = "/test"
        epoch_time = base_epoch_time

        # Exceed per-second limit but within burst limit
        for i in range(DEFAULT_LIMIT_PER_SECOND + 1):
            api_data = ApiData(
                api_key=api_key, api_route=api_route, epoch_time=epoch_time
            )
            rate_limiter.increase_incoming_request_count(api_data)

        # Should be allowed due to burst limit (even though per-second limit is exceeded)
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=epoch_time)
        assert rate_limiter.is_request_allowed(api_data) is True

        # But if we exceed burst limit too, should be blocked
        # First create enough bursts
        for burst_num in range(DEFAULT_NUMBER_OF_BURST_PER_MINUTE):
            burst_epoch = base_epoch_time + burst_num
            for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
                api_data = ApiData(
                    api_key=api_key, api_route=api_route, epoch_time=burst_epoch
                )
                rate_limiter.increase_incoming_request_count(api_data)

        # Now try to exceed both limits
        new_epoch = base_epoch_time + DEFAULT_NUMBER_OF_BURST_PER_MINUTE
        for i in range(DEFAULT_BURST_LIMIT_PER_SECOND + 1):
            api_data = ApiData(
                api_key=api_key, api_route=api_route, epoch_time=new_epoch
            )
            rate_limiter.increase_incoming_request_count(api_data)

        # Should be blocked
        api_data = ApiData(api_key=api_key, api_route=api_route, epoch_time=new_epoch)
        assert rate_limiter.is_request_allowed(api_data) is False
