from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime

from app.core.exceptions import not_found, forbidden
from app.models import User
from app.schemas.user import UserPatch, UserAdminPatch
from app.core.security import hash_password
from app.core.pagination import paginate

def _get_user_or_404(
    id: int, 
    db: Session
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        not_found("user not found")
    return user

def get_all_users(
    user: User, 
    db: Session, 
    role: Literal["admin", "operator", "viewer"] | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    page: int = 1, 
    size: int = 20, 
):    
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if start:
        query = query.filter(User.created_at >= start)
    if end:
        query = query.filter(User.created_at <= end)

    return paginate(query, page, size)

def get_user_by_id(
    id: int,
    user: User, 
    db: Session
): 
    user = _get_user_or_404(id, db)    
    return user

def get_current_user_profile(
    user: User,
):
    return user

def update_user_me(
    id: int, 
    data: UserPatch,
    db: Session
):
    user = _get_user_or_404(id, db)
    update_data = data.model_dump(exclude_none=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def update_user_by_admin(
    id: int, 
    data: UserAdminPatch,
    db: Session
):
    user = _get_user_or_404(id, db)    
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user