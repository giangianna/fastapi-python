from loguru import logger
import os

# Konfigurasi path log
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/api.log")

# Konfigurasi logger dengan rotasi dan kompresi
logger.add(
    LOG_FILE_PATH, 
    rotation="10MB",  # Rotasi setiap 10MB
    compression="zip",  # Kompresi log lama
    format="{time} | {level} | {message}"
)

def log_request(method: str, url: str, status_code: int, ip: str, response_time: float):
    """
    Logging semua request, termasuk status di luar 200.
    """
    if status_code >= 500:
        log_level = "ERROR"  # Server error
    elif status_code >= 400:
        log_level = "WARNING"  # Client error
    else:
        log_level = "INFO"  # Sukses
    
    logger.log(log_level, f"{method} {url} | Status: {status_code} | IP: {ip} | Time: {response_time:.3f}s")
