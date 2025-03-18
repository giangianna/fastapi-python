# app/middlewares/apigate_middleware.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from app.core.security import decode_access_token
import time

# Rate limiter sederhana
rate_limit_store = {}

# Daftar path yang tidak perlu API Gateway Key
EXCLUDED_PATHS = ["/", "/docs", "/openapi.json", "/favicon.ico", "/redoc", "/login"]	 

class APIGateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 🛑 Skip Middleware untuk EXCLUDED_PATHS
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)
        
        # 🔒 API Gateway Authentication
        gateway_key = request.headers.get("X-API-GATEWAY-KEY")
        if gateway_key != settings.API_GATEWAY_KEY:
            return JSONResponse(status_code=403, content={"detail": "Invalid API Gateway Key"})
        
        # 🔑 JWT Authentication
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

        token = token.split("Bearer ")[1]
        payload = decode_access_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        # 📈 Rate Limiting
        client_ip = request.client.host
        current_time = time.time()

        if client_ip in rate_limit_store:
            last_request_time, request_count = rate_limit_store[client_ip]
            if current_time - last_request_time < 60:
                if request_count >= settings.RATE_LIMIT:
                    return JSONResponse(status_code=429, content={"detail": "Too many requests"})
                rate_limit_store[client_ip] = (last_request_time, request_count + 1)
            else:
                rate_limit_store[client_ip] = (current_time, 1)
        else:
            rate_limit_store[client_ip] = (current_time, 1)

        # 📝 Logging request
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.url} from {client_ip}")

        return await call_next(request)
