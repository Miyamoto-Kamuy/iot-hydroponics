from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, LoginRequest, LoginResponse
from app.services.auth import register_user, login_user

router = APIRouter()

@router.post(
    "/auth/register", 
    response_model=UserResponse
)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post(
    "/auth/login", 
    response_model=LoginResponse
)
def login(
    data: LoginRequest, 
    db: Session = Depends(get_db)
): 
    return login_user(data, db)

@router.post("/auth/logout")
def logout(): 
    return {"message": "logged out successfully"}