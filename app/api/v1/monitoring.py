# app/api/v1/monitoring.py

from fastapi import APIRouter
from app.middlewares.apigate_middleware import api_stats

router = APIRouter()

@router.get("/monitoring")
async def get_monitoring():
    return {
        "total_requests": api_stats["total_requests"],
        "status_counts": api_stats["status_counts"],
        "average_response_time": f"{api_stats['average_response_time']:.3f} seconds"
    }
