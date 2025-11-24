from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    hashed_password:str = Field(..., alias="password")


class PostBase(BaseModel):
    title:str
    content:str


class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PostUpdate(PostBase):
    pass
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    posts: Optional[list[PostResponse]] = None
    is_active: bool
    
    class Config:
        from_attributes = True