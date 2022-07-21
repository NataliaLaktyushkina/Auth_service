import datetime
from functools import wraps
from http import HTTPStatus

from flask import jsonify, request

from database.redis_db import redis_app
from utils.logger import logger


REQUEST_LIMIT_PER_MINUTE = 30
LIMIT_IN_SECONDS = 60


class TokenBucket:

    def __init__(self):
        """
        Initially bucket is full

        """
        self.bucket_size = 30
        self.last_updated_time = datetime.datetime.now()
        self.refresh_rate = REQUEST_LIMIT_PER_MINUTE  # how many tokens refresh in interval
        self.interval = LIMIT_IN_SECONDS  # n 'refresh_rate' tokens per m 'interval' seconds
        self.current_capacity = self.bucket_size

    def rate_limit(self):
        """Rate limit for API endpoints.

        If the user has exceeded the limit, then return the response 429.

        Cost of request = 1 (default)
        Check that in bucket there are more tokens than request cost
        """

        def rate_limit_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                self.refresh_bucket()
                now = datetime.datetime.now()
                key = f"{request.remote_addr}:{now.minute}"

                current_request_count = redis_app.get(key)

                if current_request_count and int(current_request_count) > self.bucket_size:
                    logger.info(f"Hitting rate limit: {key}")
                    response = jsonify(
                        {
                            "code": HTTPStatus.TOO_MANY_REQUESTS,
                            "message": f"Too many requests."
                            f"Limit {self.refresh_rate} in {self.interval} seconds",
                        }
                    )
                    response.status_code = HTTPStatus.TOO_MANY_REQUESTS

                    return response
                else:
                    pipe = redis_app.pipeline()
                    pipe.incr(key, 1)
                    pipe.expire(key, self.interval - 1)
                    pipe.execute()

                    return f(*args, **kwargs)

            return wrapper

        return rate_limit_decorator

    def refresh_bucket(self):
        """
        Calculate how may tokens should add to buket
        There should be tokens no more than bucket size
        """
        current_time = datetime.datetime.now()
        additional_tokens = int((current_time - self.last_updated_time).seconds * self.refresh_rate/self.interval)
        current_capacity = min(self.bucket_size, self.current_capacity + additional_tokens)
        self.current_capacity = current_capacity
        self.last_updated_time = current_time


token_bucket = TokenBucket()
