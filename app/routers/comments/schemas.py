from datetime import datetime
from typing import Optional
from pydantic import BaseModel

DEFAULT_LIKES_AMOUNT = 0


class CommentBase(BaseModel):
    content: str
    
    class Config:
        from_attributes = True


class GetComment(CommentBase):
    id: int
    author_id: int
    blog_id: int
    created_at: datetime
    likes_count: Optional[int] = DEFAULT_LIKES_AMOUNT

    class Config:
        from_attributes = True


class CreateComment(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass
