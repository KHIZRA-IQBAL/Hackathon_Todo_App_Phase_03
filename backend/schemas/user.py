from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime  # ✅ Add this import

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int  # ✅ Changed from str to int
    email: str
    full_name: Optional[str] = None
    created_at: datetime  # ✅ Changed from str to datetime
    
    class Config:
        from_attributes = True

class UserUpdateProfile(BaseModel):
    full_name: Optional[str] = None