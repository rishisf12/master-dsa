from fastapi import APIRouter, HTTPException
from app.schemas.auth import AuthRequest, AuthResponse
from app.core.security import verify_admin_username

router = APIRouter()


@router.post("/auth/verify", response_model=AuthResponse)
async def verify_admin(request: AuthRequest):
    """Verify admin username."""
    if verify_admin_username(request.username):
        return {
            "valid": True,
            "message": "Username verified successfully"
        }
    else:
        return {
            "valid": False,
            "message": "Invalid username"
        }