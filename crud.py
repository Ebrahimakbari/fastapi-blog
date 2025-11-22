from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Post
from serializers import UserCreate, UserResponse, PostCreate, PostResponse, PostUpdate
from typing import Optional
from pydantic import EmailStr


class UserCrud:
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email:EmailStr) -> Optional[User]:
        user = await db.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: int) -> Optional[User]:
        user = await db.execute(select(User).where(User.id == id))
        return user.scalar_one_or_none()
    
    @staticmethod
    async def create_user(db: AsyncSession, user:UserCreate):
        db_user = User(
            email=user.email,
            hashed_password=user.password,
            posts = []
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

        

class PostCrud:
    
    @staticmethod
    async def get_posts(db: AsyncSession, skip:int = 0, limit:int = 10) -> list[Post]:
        posts = await db.execute(
            select(Post).offset(skip).limit(limit).order_by(Post.created_at.desc())
        )
        return posts.scalars().all()
    
    @staticmethod
    async def get_post(db: AsyncSession, post_id:int):
        post = await db.execute(select(Post).where(Post.id == post_id))
        return post.scalar_one_or_none()

    @staticmethod
    async def create_post(db: AsyncSession, post: PostCreate, owner_id: int):
        db_post = Post(
            **post.model_dump(),
            owner_id=owner_id
        )
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post
    
    @staticmethod
    async def update_post(db: AsyncSession, post_id:int, post:PostUpdate):
        existing_post = await PostCrud.get_post(db, post_id)
        if not existing_post:
            return None
        updated_data = post.model_dump(exclude_unset=True)
        if updated_data:
            db.execute(
                update(Post).where(Post.id == post_id).values(**updated_data)
            )
            await db.commit()
            await db.refresh(existing_post)
        return existing_post

    @staticmethod
    async def delete_post(db:AsyncSession, post_id:int):
        post = await PostCrud.get_post(db, post_id)
        if not post:
            return False
        
        await db.execute(delete(Post).where(Post.id == post_id))
        await db.commit()
        return True
    
    @staticmethod
    async def get_user_posts(db:AsyncSession, user_id: int):
        posts = await db.execute(select(Post).where(Post.owner_id == user_id).order_by(Post.created_at.desc()))
        return posts.scalars().all()
        