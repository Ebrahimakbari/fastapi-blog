from db import Base
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    post = relationship("Post", back_populates='owner', cascade='all, delete-orphan')

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates='posts')