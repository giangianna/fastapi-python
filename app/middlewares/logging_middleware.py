import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.utils.logger import log_request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response: Response = await call_next(request)

        process_time = time.time() - start_time
        log_request(
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            ip=request.client.host if request.client else "unknown",
            response_time=process_time
        )

        return response
