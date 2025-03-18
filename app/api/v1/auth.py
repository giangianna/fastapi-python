# app/api/v1/auth.py

from fastapi import APIRouter, HTTPException, Depends
from app.core.security import create_access_token, verify_password, hash_password
from datetime import timedelta
from pydantic import BaseModel

router = APIRouter()

# Simulasi database pengguna
fake_users_db = {
    "admin": {"username": "admin", "password": hash_password("admin123")}
}

# Schema untuk login
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = fake_users_db.get(request.username)
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": request.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token}
