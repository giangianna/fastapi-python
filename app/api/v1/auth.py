# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.core.config import settings
import bcrypt
from jose import jwt, JWTError
from pydantic import BaseModel

# Simulasi database pengguna (sebaiknya pakai database nyata)
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    }
}

# Simulasi penyimpanan refresh token (HARUS diganti dengan database dalam produksi)
FAKE_REFRESH_TOKENS = {}

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse, summary="Login untuk mendapatkan JWT Token", tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint untuk mendapatkan JWT access token dengan username dan password.
    """

    username = form_data.username
    password = form_data.password

    # Periksa apakah username ada dalam database
    user = FAKE_USERS_DB.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Buat access token & refresh token
    access_token = create_access_token(
        data={"sub": username}, 
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": username}, 
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Simpan refresh token (sebaiknya di database)
    FAKE_REFRESH_TOKENS[username] = refresh_token

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse, summary="Refresh access token menggunakan refresh token", tags=["Authentication"])
async def refresh_access_token(request: RefreshTokenRequest):
    """
    Endpoint untuk memperbarui access token dengan menggunakan refresh token.
    """
    refresh_token = request.refresh_token
    print(f"Received refresh token: {refresh_token}")  # DEBUG
    
    try:
        # Decode refresh token
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")

        print(f"Decoded username from token: {username}, Exp: {exp}")  # DEBUG

        if not username or FAKE_REFRESH_TOKENS.get(username) != refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Periksa apakah refresh token telah kedaluwarsa
        if datetime.utcnow().timestamp() > exp:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Hapus refresh token lama untuk keamanan (opsional)
        del FAKE_REFRESH_TOKENS[username]

        # Buat access token baru
        new_access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        # Buat refresh token baru untuk menggantikan yang lama
        new_refresh_token = create_refresh_token(
            data={"sub": username},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        # Simpan refresh token baru di database (simulasi)
        FAKE_REFRESH_TOKENS[username] = new_refresh_token

        return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    
    except JWTError as e:
        print(f"JWT Error: {e}")  # DEBUG
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
