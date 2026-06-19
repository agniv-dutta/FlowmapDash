import time
import logging
from flask import request, g

logger = logging.getLogger(__name__)


def register_middleware(app):
    @app.before_request
    def before_request():
        g.start_time = time.perf_counter()
        g.request_id = request.headers.get("X-Request-Id", "-")

    @app.after_request
    def after_request(response):
        duration = time.perf_counter() - g.get("start_time", time.perf_counter())
        request_id = g.get("request_id", "-")

        logger.info(
            "%s %s %s %s %.3f",
            request_id,
            request.method,
            request.path,
            response.status_code,
            duration,
        )

        response.headers.add("X-Response-Time-Ms", round(duration * 1000, 1))
        response.headers.add("X-Request-Id", request_id)

        return response
