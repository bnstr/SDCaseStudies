class RateLimiter:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size

    def is_allowed(self, client_id):
        raise NotImplementedError("Subclasses should implement this!")

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, limit, window_size):
        super().__init__(limit, window_size)
        self.request_counts = {}

    def is_allowed(self, client_id):
        current_window = self.get_key(client_id)
        if current_window not in self.request_counts:
            self.request_counts[current_window] = 0
        if self.request_counts[current_window] < self.limit:
            self.request_counts[current_window] += 1
            return True
        return False

    def get_key(self, client_id):
        return f"{client_id}:{int(time.time() // self.window_size)}"

class RateLimiterFactory:
    def create_rate_limiter(self, strategy, limit, window_size):
        if strategy == "fixed_window":
            return FixedWindowRateLimiter(limit, window_size)
        # Add additional strategies here.
        raise ValueError("Unknown strategy")

# Example usage:
rate_limiter_factory = RateLimiterFactory()
rate_limiter = rate_limiter_factory.create_rate_limiter("fixed_window", 100, 60)

if rate_limiter.is_allowed("client_1"):
    print("Request allowed")
else:
    print("Request denied")
