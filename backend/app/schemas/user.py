from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
