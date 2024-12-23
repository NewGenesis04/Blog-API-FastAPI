from pydantic import BaseModel
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
    author: "UserSummary"

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
    email: str
    role: Optional[str] = "author"

    class Config:
        from_attributes = True
        extra = "forbid"


class UserDelete(UserBase):
    pass

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass


class UserSummary(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

BlogSummary.model_rebuild() #This is because the usersummary hasn't beeen defined when it was called


class User(UserBase):
    id: int
    blogs: List[BlogSummary] = []

    class Config:
        from_attributes = True