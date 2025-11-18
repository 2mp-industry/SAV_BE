from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
import uuid
from core.enums import UserRole

class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True 

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.VIEWER
"""
    @validator('password')
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
        

    class Config:
        use_enum_values = True  # AJOUTEZ CE CONFIG IMPORTANT

        """