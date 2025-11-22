from sqlalchemy.ext.asyncio import AsyncSession
from serializers import UserCreate, UserResponse, PostCreate, PostResponse, PostUpdate
from crud import PostCrud, UserCrud
from fastapi import Depends, HTTPException, status
from db import get_db



async def create_user_api(user:UserCreate, db:AsyncSession = Depends(get_db)):
    existing_user = await UserCrud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='email already exists!!')
    
    new_user = await UserCrud.create_user(db, user)
    return new_user


async def create_post_api(post: PostCreate, user_id:int, db:AsyncSession = Depends(get_db)):
    exist_user = await UserCrud.get_user_by_id(db, user_id)
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='there is no user with that id'
        )
    new_post = await PostCrud.create_post(db, post, user_id)
    return new_post