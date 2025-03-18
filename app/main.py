# app/main.py

from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router
from app.api.v1.auth import router as auth_router
from app.middlewares.apigate_middleware import APIGateMiddleware

app = FastAPI(title="Swamedia API Gateway")

# 🛡️ Tambahkan Middleware APIGate
app.add_middleware(APIGateMiddleware)

# 🔗 Tambahkan Router API
app.include_router(api_router, prefix="/api/v1")
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Swamedia API Gateway!"}
