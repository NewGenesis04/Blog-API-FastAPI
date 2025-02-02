from unittest.mock import Base
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# Pydantic Schema for Blog
class BlogBase(BaseModel):
    title: str
    content: str
    published_at: Optional[datetime] = None
    published: bool = False

    class Config:
        from_attributes = True
        extra = "forbid"

class BlogCreate(BlogBase):
    author_id: Optional[int] = None
    class Config:
        from_attributes = True
        extra = "forbid"

class BlogUpdate(BaseModel): 
    title: str
    content: str
    published: bool = False

    class Config:
        from_attributes = True
        extra = "forbid"

class BlogSummary(BaseModel):  # summarised blog response model.
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True


class Blog(BlogBase):
    id: int
    author_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True  # Tells Pydantic to treat SQLAlchemy models like dicts
        extra = "forbid"


# Pydantic Schema for User
class UserBase(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
        extra = "forbid"

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "author"

class UserUpdate(UserBase):
    password: Optional[str] = None
    role: Optional[str] = "author"
    pass


class UserSummary(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    blogs: List[BlogSummary] = []

    class Config:
        from_attributes = True


class FollowBase(BaseModel):
    pass

class Follow(FollowBase):
    follower_id: int
    followed_id: int
    
    class Config:
        from_attributes = True

class Unfollow(FollowBase):
    follower_id: int
    followed_id: int
    
    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str
    
    class Config:
        from_attributes = True

class GetComment(CommentBase):
    id: int
    author_id: int
    blog_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CreateComment(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass
    