# app/api/v1/endpoints.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/protected")
async def protected_endpoint():
    return {"message": "Access granted to protected endpoint"}
