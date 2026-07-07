from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserResponse, UserPatch, UserAdminPatch
from app.services.user import get_all_users, get_current_user_profile, get_user_by_id, update_user_me, update_user_by_admin
from app.core.deps import get_current_user, require_role
from app.models import User
from typing import Literal
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/", 
    response_model=list[UserResponse]
)
def get_users(
    user: User = Depends(require_role("admin")), 
    db: Session = Depends(get_db), 
    role: Literal['admin', 'operator', 'viewer'] | None = None, 
    start: datetime | None = None, 
    end: datetime | None = None,
):
    return get_all_users(user, db, role, start, end)

@router.get(
    "/me", 
    response_model=UserResponse
)
def get_user_profile(
    user: User = Depends(get_current_user),     
):
    return get_current_user_profile(user)

@router.get(
    "/{id}", 
    response_model=UserResponse
)
def get_user(
    id: int,
    user: User = Depends(require_role("admin")), 
    db: Session = Depends(get_db)
):
    return get_user_by_id(id, user, db)

@router.patch(
    "/me", 
    response_model=UserResponse
)
def update_user_profile(    
    data: UserPatch, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_user_me(user.id, data, db) 

@router.patch(
    "/{id}", 
    response_model=UserResponse, 
    dependencies=[Depends(require_role("admin"))]
)
def update_user(
    id: int, 
    data: UserAdminPatch, 
    db: Session = Depends(get_db)
):
    return update_user_by_admin(id, data, db)
