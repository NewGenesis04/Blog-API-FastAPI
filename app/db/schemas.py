from unittest.mock import Base
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime


class AuthPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

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
    tag: Optional[str] = None

    @field_validator("tag")
    @classmethod
    def lowercase_and_validate_tag(cls, v):
        allowed_tags = {"entertainment", "technology", "health & wellness", "lifestyle"}
        v = v.lower() if v else v
        if v and v not in allowed_tags:
            raise ValueError(f"Invalid tag '{v}'. Allowed tags: {allowed_tags}")
        return v
    
    class Config:
        from_attributes = True
        extra = "forbid"

class BlogUpdate(BaseModel): 
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    published_at: Optional[datetime] = None
    tag: Optional[str] = None

    @field_validator("tag")
    @classmethod
    def lowercase_and_validate_tag(cls, v):
        allowed_tags = {"entertainment", "technology", "health & wellness", "lifestyle"}
        v = v.lower() if v else v
        if v and v not in allowed_tags:
            raise ValueError(f"Invalid tag '{v}'. Allowed tags: {allowed_tags}")
        return v
    

    class Config:
        from_attributes = True 
        extra = "forbid"

class BlogSummary(BaseModel):  # summarised blog response model.
    id: int
    title: str
    content: str
    author_id: int
    tag: Optional[str]

    class Config:
        from_attributes = True


class Blog(BlogBase):
    id: int
    author_id: Optional[int] = None
    created_at: datetime
    tag: Optional[str] = None

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

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    bio: Optional[str] = None


class UserSummary(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    profile_url: Optional[str] = None

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    role: str
    profile_url: Optional[str] = None
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
    