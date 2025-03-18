# app/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token
import bcrypt  # Library untuk hashing password

# Simulasi database pengguna (seharusnya dari database)
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")  # Hash password
    }
}

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Memeriksa apakah password yang dimasukkan sesuai dengan password yang telah di-hash.

    :param plain_password: Password yang dimasukkan pengguna
    :param hashed_password: Password hash yang tersimpan
    :return: True jika password cocok, False jika tidak
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

@router.post("/login", summary="Login untuk mendapatkan JWT Token", tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint untuk mendapatkan JWT access token dengan menggunakan username dan password.

    ### Request:
    - `username`: Username pengguna
    - `password`: Password pengguna

    ### Response:
    - `access_token`: Token yang digunakan untuk autentikasi
    - `token_type`: Jenis token (bearer)

    ### Keamanan:
    - Password disimpan dalam bentuk hashed menggunakan bcrypt.
    - Hashing dilakukan agar password tidak disimpan dalam bentuk plaintext.
    """

    username = form_data.username
    password = form_data.password

    # Periksa apakah username ada dalam database
    user = FAKE_USERS_DB.get(username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Verifikasi password menggunakan bcrypt
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Buat token akses dengan payload `sub` berisi username
    access_token = create_access_token(
        data={"sub": username},  # Subjek token (pengguna)
        expires_delta=timedelta(minutes=30)  # Token berlaku selama 30 menit
    )

    return {"access_token": access_token, "token_type": "bearer"}
