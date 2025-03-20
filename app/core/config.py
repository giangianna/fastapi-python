# app/core/config.py

import os
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

class Settings:
    """
    Konfigurasi aplikasi yang diambil dari file .env.
    """
    PROJECT_NAME: str = "Swamedia APIGate"
    API_GATEWAY_KEY: str = os.getenv("API_GATEWAY_KEY", "default-secret-key")
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", 5))  # Maksimum request per menit
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey123")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Inisialisasi pengaturan yang bisa digunakan di seluruh aplikasi
settings = Settings()
