# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Swamedia APIGate"
    API_GATEWAY_KEY: str = os.getenv("API_GATEWAY_KEY", "default-secret-key")
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", 100))  # Maksimum request per menit

settings = Settings()
