from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Literal, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["operator", "viewer"] = "viewer"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    model_config=ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserPatch(BaseModel):    
    password: Optional[str] = None    

class UserAdminPatch(BaseModel):
    role: Optional[Literal["admin", "operator", "viewer"]] = None