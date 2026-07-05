from sqlalchemy.orm import Session
from app.core.exceptions import bad_request, unauthorised

from app.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, LoginRequest
from app.core.config import settings

def register_user(
    user: UserCreate, 
    db: Session
):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        bad_request("email already registered")

    new_user = User(
        email = user.email, 
        hashed_password = hash_password(user.password), 
        role = user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(
    data: LoginRequest, 
    db: Session
): 
    user = db.query(User).filter(
        User.email == data.email
    ).first()
    if not user:
        unauthorised("incorrect email or password")
    if not verify_password(data.password, user.hashed_password):
        unauthorised("incorrect email or password")
    
    access_token = create_access_token(
        {
            "user_id": user.id
        }
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }