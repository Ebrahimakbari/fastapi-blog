from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password:str


    


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
        from_attribute = True


class PostUpdate(PostBase):
    pass
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    posts: list[PostResponse] = None
    is_active: bool
    
    class Config:
        from_attribute = True