import unittest
import time

class RateLimiter:
    def __init__(self, limit, time_frame):
        self.limit = limit
        self.time_frame = time_frame

    def isAllow(self, requestId):
        raise NotImplementedError("Subclasses should implement this!")

class FixedWindowRateLimiter(RateLimiter):

    def __init__(self, limit, time_frame):
        super().__init__(limit, time_frame)
        self.request_counts = {}

        # request_counts {key : value }
        # key: requestId
        # value:  list of timestamps    ( only the ones in time_frame)
        # {'id_123': [1723226883.1192372, 1723226883.119375, 1723226883.119487, 1723226883.119602]}

    def isAllow(self, requestId):

        # only track request counts that are within the correct time_frame
        # VALID timeframe is  current_window-self.time_frame
        current_time = time.time()
        valid_timeframe = current_time - self.time_frame

        if requestId not in self.request_counts:
            self.request_counts[requestId] = []

        # Filter timestamps for the given requestId to only include those within the valid timeframe
        valid_timestamp_counts = [timestamp for timestamp in self.request_counts[requestId] if timestamp > valid_timeframe]

        # Update the request counts {} values to only account for the latest valid_timestamps (will drop all values not in valid interval)
        self.request_counts[requestId] = valid_timestamp_counts

        # Check if the number of valid requests exceeds the limit, "fail-fast" principle
        if len(valid_timestamp_counts) >= self.limit:
            return False

        # Allow the request and add the current timestamp
        self.request_counts[requestId].append(current_time)
        print(f"self.request_counts {self.request_counts}")
        return True


class SlidingWindowRateLimiter(RateLimiter):
    def __init__(self, limit, time_frame):
        pass

    def isAllow(self, requestId):
        pass

class RateLimiterFactory:
    def create_rate_limiter(self, strategy, limit, time_frame):
        if strategy == "fixed_window":
            return FixedWindowRateLimiter(limit, time_frame)
        # Add additional strategies here.
        raise ValueError("Unknown strategy")

#####################################################
class RateLimiterTest(unittest.TestCase):

    def setUp(self):
        rate_limiter_factory = RateLimiterFactory()
        self.rate_limiter = rate_limiter_factory.create_rate_limiter("fixed_window", 10, 1)

    def test_allow_request_within_limit(self):
        client_id = "id_123"
        for i in range(10):
            self.assertTrue(self.rate_limiter.isAllow(client_id), "fails test_allow_request_within_limit")


    def test_deny_request_exceeding_limit(self):
        client_id = "id_123"
        for i in range(100):
            self.rate_limiter.isAllow(client_id)
        self.assertFalse(self.rate_limiter.isAllow(client_id), "Request 101 should be denied")

    def test_allow_requests_after_time_frame(self):
        client_id = "id_123"
        for i in range(100):
            self.rate_limiter.is_allow(client_id)
        time.sleep(1)  # Wait for the time frame to reset
        self.assertTrue(self.rate_limiter.isAllow(client_id), "Request after time frame should be allowed")

    def test_multiple_clients(self):
        pass

    def test_requests_after_partial_time_frame(self):
        pass
