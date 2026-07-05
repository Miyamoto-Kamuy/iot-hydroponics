from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["operator", "viewer"] = "viewer"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int