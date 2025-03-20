from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from app.core.security import decode_access_token
import time
import logging

# Statistik API (Monitoring)
api_stats = {
    "total_requests": 0,
    "status_counts": {},
    "average_response_time": 0
}

# Rate limiter sederhana
rate_limit_store = {}

# Daftar path yang tidak perlu API Gateway Key
EXCLUDED_PATHS = ["/", "/docs", "/openapi.json", "/favicon.ico", "/redoc", "/login", "/monitoring"]  

logger = logging.getLogger(__name__)

class APIGateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # 🛑 **Skip Middleware untuk EXCLUDED_PATHS**
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        try:
            start_time = time.time()
            client_ip = request.client.host

            # 🔒 **API Gateway Authentication**
            gateway_key = request.headers.get("X-API-GATEWAY-KEY")
            if gateway_key != settings.API_GATEWAY_KEY:
                logger.warning(f"🚨 Invalid API Gateway Key from {client_ip}")
                return JSONResponse(status_code=403, content={"detail": "Invalid API Gateway Key"})

            # 🔑 **JWT Authentication**
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                logger.warning(f"🔑 Missing or invalid token from {client_ip}")
                return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

            token = token.split("Bearer ")[1]
            payload = decode_access_token(token)
            if not payload:
                logger.warning(f"❌ Invalid or expired token from {client_ip}")
                return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

            # 📈 **Rate Limiting**
            current_time = time.time()

            if client_ip in rate_limit_store:
                last_request_time, request_count = rate_limit_store[client_ip]

                if current_time - last_request_time < 60:
                    if request_count >= settings.RATE_LIMIT:
                        logger.warning(f"⛔ Too many requests from {client_ip}")
                        return JSONResponse(status_code=429, content={"detail": "Too many requests"})

                    rate_limit_store[client_ip] = (last_request_time, request_count + 1)
                else:
                    rate_limit_store[client_ip] = (current_time, 1)  # Reset request count jika lebih dari 60 detik
            else:
                rate_limit_store[client_ip] = (current_time, 1)

            # 📝 **Logging request**
            logger.info(f"📌 [{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.url} from {client_ip}")

            # 🔄 **Eksekusi request**
            response = await call_next(request)

            # 🔍 **Hitung response time**
            response_time = time.time() - start_time

            # 📊 **Update statistik API**
            api_stats["total_requests"] += 1
            status_code = response.status_code
            api_stats["status_counts"][status_code] = api_stats["status_counts"].get(status_code, 0) + 1
            api_stats["average_response_time"] = (api_stats["average_response_time"] + response_time) / 2

            # 📝 **Logging response**
            logger.info(f"✅ Response {status_code} for {request.method} {request.url.path} in {response_time:.4f}s")

            return response

        except Exception as e:
            logger.error(f"❌ Middleware error: {e}", exc_info=True)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error in Middleware"})
