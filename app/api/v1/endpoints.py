# app/api/v1/endpoints.py

from fastapi import APIRouter, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from app.core.security import decode_access_token

router = APIRouter()

# Header untuk API Gateway Key
api_key_header = APIKeyHeader(name="X-API-GATEWAY-KEY", auto_error=False)

# OAuth2 untuk JWT Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_jwt(token: str = Security(oauth2_scheme)):
    """
    Verifikasi JWT Token sebelum mengakses endpoint yang dilindungi.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.get(
    "/protected",
    summary="Protected API Endpoint",
    description="""
    Endpoint ini hanya dapat diakses oleh pengguna dengan API Gateway Key dan JWT yang valid.
    
    **Authorization:**
    - Tambahkan **X-API-GATEWAY-KEY** di header.
    - Tambahkan **Bearer Token (JWT)** di header Authorization.

    **Rate Limit:**
    - Maksimal **5 request per menit**.
    
    **Response Status:**
    - ✅ `200 OK`: Berhasil mengakses endpoint.
    - ❌ `401 Unauthorized`: JWT tidak valid atau kadaluarsa.
    - ❌ `403 Forbidden`: API Gateway Key salah atau tidak diberikan.
    - ❌ `429 Too Many Requests`: Melebihi batas rate limit.
    """,
    responses={
        200: {"description": "Access granted to protected endpoint"},
        401: {"description": "Invalid or expired token"},
        403: {"description": "Invalid API Gateway Key"},
        429: {"description": "Too many requests"}
    }
)
async def protected_endpoint(
    api_key: str = Security(api_key_header),
    token_data: dict = Depends(verify_jwt)
):
    """
    Mengembalikan response sukses jika API Key dan JWT valid.
    """
    if api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API Gateway Key")

    return {"message": "Access granted to protected endpoint"}
