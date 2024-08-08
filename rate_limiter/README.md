
## Object-oriented design for a API Rate Limiter.
#### Types of limits
* **Fixed Window**: A simple counter resets after a fixed interval (e.g., 100 requests per minute).
* **Sliding Window**: Counts requests in the last N seconds.
* **Token Bucket**: Tokens are added at a regular rate, and each request consumes a token.


### 1) Define Requirements
####   Functional Requirements:
* **Rate Limiting**: The system should enforce rate limits on API calls based on different strategies.
* **Multiple Strategies**: Support for various rate-limiting strategies like Fixed Window, Sliding Window, and Token Bucket.
* **Thread-Safety**: Ensure that the rate limiter can handle concurrent requests in a multi-threaded environment.
* **Extensibility**: The system should allow easy addition of new rate-limiting strategies.

####   Non-Functional Requirements:
* **Scalability**: The system should scale to handle thousands of API requests per second.
* **Low Latency**: Rate checks should introduce minimal latency to API requests.
* **Persistence**: Optionally store rate limit data in a distributed cache like Redis for scalability.

### 2) Identify Key Entities
   From the requirements, we can identify the following key entities:
* **Client**: Represents the user or application making API requests.
* **RateLimiter**: Abstract base class defining the common interface for rate-limiting strategies.
* **FixedWindowRateLimiter**: A rate limiter using the Fixed Window strategy.
* **SlidingWindowRateLimiter**: A rate limiter using the Sliding Window strategy.
* **TokenBucketRateLimiter**: A rate limiter using the Token Bucket strategy.
* **RateLimiterFactory**: Factory class to create instances of different rate limiters.
* **Request**: Represents an API request made by a client.
### 3) Design Class Structure

* Class: RateLimiter
```
Attributes:
limit: int (Maximum allowed requests)
window_size: int (Time window for the rate limit in seconds)

Methods:
is_allowed(client_id: str) -> bool: Checks if the request from the client is allowed.
get_key(client_id: str) -> str: Generates a key based on client ID and time window.

```
* Class: FixedWindowRateLimiter (inherits from RateLimiter)
```
Attributes:
request_counts: dict (Mapping of client ID to request counts)
Methods:
is_allowed(client_id: str) -> bool: Implements the fixed window logic.
```
* Class: SlidingWindowRateLimiter (inherits from RateLimiter)
```
Attributes:
timestamps: dict (Mapping of client ID to list of request timestamps)
Methods:
is_allowed(client_id: str) -> bool: Implements the sliding window logic.
```
* Class: TokenBucketRateLimiter (inherits from RateLimiter)
```
Attributes:
tokens: dict (Mapping of client ID to token counts)
last_request_time: dict (Mapping of client ID to the last request time)
Methods:
is_allowed(client_id: str) -> bool: Implements the token bucket logic.
add_tokens(client_id: str) -> None: Adds tokens to the bucket based on elapsed 
```
* Class: RateLimiterFactory
```
Methods:
create_rate_limiter(strategy: str, limit: int, window_size: int) -> RateLimiter: Factory method to create rate limiter instances.
```

### 4) Sequence Diagrams
Request Flow:
1) Client sends a request to the API.
2) The API checks the RateLimiter instance for the client.
3) The RateLimiter determines if the request is allowed based on the implemented strategy.
4) If allowed, the request is processed; otherwise, the request is rejected.


