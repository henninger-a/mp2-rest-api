import logging
import time
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """Log one request and attach its request ID to the response."""
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.error(f"Unexpected failure: request_id={request_id}", exc_info=True)
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    duration_ms = (time.perf_counter() - started) * 1000

    message = (f"request id:{request_id} request method: {request.method} url path: {request.url.path} "
        f"status: {response.status_code} duration: {duration_ms}ms")
  
    if 400 <= response.status_code < 500:
        logger.warning(message)
    elif 500 <= response.status_code < 600:
        logger.error(message)
    else:
        logger.info(message)

    response.headers["X-Request-ID"] = request_id
    return response
