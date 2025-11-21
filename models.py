from sqlalchemy import String, Column, Integer, ForeignKey, Boolean, DateTime, func, Float, Table, Enum, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum
from sqlalchemy.sql import func


class FileTypes(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"


post_files = Table(
    'post_files',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('file_id', Integer, ForeignKey('files.id', ondelete='CASCADE'), primary_key=True)
)


user_followers = Table(
    'user_followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
)



class User(Base):
    __table_name__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    files = relationship("File", back_populates="owner", cascade="all, delete-orphan")
    avatar = relationship("File", back_populates="user_avatar", uselist=False)

    followers = relationship(
        "User", 
        secondary=user_followers,
        primaryjoin=id == user_followers.c.follower_id,
        secondaryjoin=id == user_followers.c.following_id,
        backref='following'
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500))
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    files = relationship("File", secondary=post_files, back_populates="posts")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    parent_comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))

    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    mime_type = Column(String(100), nullable=False)
    file_type = Column(Enum(FileTypes), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user_avatar_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    owner = relationship("User", back_populates="files", foreign_keys=[owner_id])
    user_avatar = relationship("User", back_populates="avatar", foreign_keys=[user_avatar_id])
    posts = relationship("Post", secondary=post_files, back_populates="files")