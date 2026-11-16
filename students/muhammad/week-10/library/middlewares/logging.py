from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggerMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        beginning = time.perf_counter()
        response = await call_next(request)
        total_time = time.perf_counter() - beginning
        logger.info(f"""\n\t\t---New Request---
    Request Method: {request.method}
    Request Path: {request.url.path}
    Response Code: {response.status_code}
    Duration: {total_time}
    """)
        return response

class UUIDLoggerMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4()
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(request_id)
        logger.info(f"Request ID: {request_id}")
        return response
