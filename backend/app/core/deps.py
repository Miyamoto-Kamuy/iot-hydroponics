from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_access_token
from app import models

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = verify_access_token(credentials.credentials)
    if not payload:
        raise credentials_exception
    
    user_id = payload.get("user_id")
    if not user_id:
        raise credentials_exception
    
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise credentials_exception
    
    return user

def require_role(*roles: str):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Permission denied"
            )
        return current_user
    return checker