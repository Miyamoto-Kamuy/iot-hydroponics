from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.services.auth import register_user, login_user
from app.core.limiter import limiter

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


@router.post(
    "/auth/login", 
    response_model=LoginResponse
)
@limiter.limit("5/minute")
def login(
    request: Request,
    data: LoginRequest, 
    db: Session = Depends(get_db)
): 
    return login_user(data, db)

@router.post("/auth/logout")
def logout(): 
    return {"message": "logged out successfully"}