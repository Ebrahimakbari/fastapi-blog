from sqlalchemy.ext.asyncio import AsyncSession
from serializers import UserCreate, UserResponse, PostCreate, PostResponse, PostUpdate
from crud import PostCrud, UserCrud
from fastapi import Depends, HTTPException, status, Body
from db import get_db
from pydantic import EmailStr



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


async def get_user_by_email_api(user_email:EmailStr , db:AsyncSession = Depends(get_db)):
    user = await UserCrud.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no user found with given email"
        )
    return user


async def get_user_by_id_api(id:int, db:AsyncSession = Depends(get_db)):
    user = await UserCrud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no user found with given user id"
        )
    return user


async def get_post_api(post_id:int, db:AsyncSession = Depends(get_db)):
    post = await PostCrud.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no post found with post id"
        )
    return post


async def get_posts_api(skip:int = 0, limit:int = 10, db:AsyncSession = Depends(get_db)) -> list[PostResponse]:
    posts = await PostCrud.get_posts(db, skip, limit)
    if not posts:
        return []
    return posts


async def update_post_api(post_id:int, post:PostUpdate, db:AsyncSession = Depends(get_db)):
    post = await PostCrud.update_post(db, post_id, post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no post with given id'
        )
    return post


async def delete_post_api(post_id:int, db:AsyncSession = Depends(get_db)):
    post = await PostCrud.delete_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='no post found with given id'
        )
    return {
        'message': 'ok'
    }


async def get_user_post_api(user_id:int, db:AsyncSession = Depends(get_db)):
    user = await UserCrud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='no user found with given id'
        )
    user_posts = await PostCrud.get_user_posts(db, user_id)
    return user_posts