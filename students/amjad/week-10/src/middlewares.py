from fastapi import Request, Response
from typing import Callable, Awaitable
import logging
import uuid

logging.basicConfig(level=logging.INFO)


async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    import time

    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    logging.info(
        f"{request.method} {request.url.path} {response.status_code} {duration}ms"
    )
    return response


async def add_request_id(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logging.info(f"Request ID: {request_id} - {request.method} {request.url.path}")
    return response
