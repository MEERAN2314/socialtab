from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    pin: str = Field(..., min_length=4, max_length=6)
    full_name: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores and hyphens allowed)')
        return v.lower()
    
    @validator('pin')
    def pin_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('PIN must contain only digits')
        return v

class UserLogin(BaseModel):
    username: str
    pin: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime
    total_owed: float = 0.0
    total_owing: float = 0.0

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
