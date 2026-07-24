from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, LoginRequest
from app.services.auth import register_user, login_user
from app.core.limiter import limiter
from app.core.config import settings

router = APIRouter()

@router.post(
    "/auth/register", 
    response_model=UserResponse
)
@limiter.limit("3/minute")
def create_user(
    request: Request,
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post("/auth/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    data: LoginRequest, 
    response: Response,
    db: Session = Depends(get_db)
): 
    result = login_user(data, db)
    response.set_cookie(
        key="token", 
        value=result["access_token"], 
        httponly=True,
        samesite="None",
        secure=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "logged in successfully"}

@router.post("/auth/logout")
def logout(response: Response): 
    response.delete_cookie("token")
    return {"message": "logged out successfully"}