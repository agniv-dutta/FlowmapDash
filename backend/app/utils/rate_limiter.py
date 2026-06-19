import time
import logging
from functools import wraps
from flask import request, jsonify, current_app

logger = logging.getLogger(__name__)


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


_buckets: dict[str, TokenBucket] = {}


def rate_limit(capacity: int = 100, refill_rate: float = 10.0):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = request.remote_addr or "unknown"
            if key not in _buckets:
                _buckets[key] = TokenBucket(capacity, refill_rate)

            bucket = _buckets[key]
            if not bucket.consume():
                logger.warning("Rate limit exceeded for %s", key)
                return jsonify({"error": "Too many requests"}), 429

            return f(*args, **kwargs)

        return wrapper

    return decorator
