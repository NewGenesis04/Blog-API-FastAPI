from email.policy import HTTP
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import User
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user
from app.services import CommentService

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['comments'])

def get_comment_service(require_user: bool = False):
    """Factory to enforce (or skip) auth dynamically per route."""
    def _get_service(                                                
        db: Session = Depends(get_db),
        current_user: Optional[schemas.User] = Depends(get_current_user) if require_user else None,
    ):
        if require_user and current_user is None:
            raise HTTPException(401, "Authentication required")
        return CommentService(db, current_user)
    return _get_service

@router.post('/{blog_id}', status_code=status.HTTP_201_CREATED)
def comment_on_blog(blog_id: int, service: CommentService = Depends(get_comment_service(True))) -> schemas.CreateComment:
    return service.comment_on_blog(blog_id)

@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
def get_comments(blog_id: int, include_all: Optional[bool] = False, author_id: Optional[int] = None, service: CommentService = Depends(get_comment_service(False))) -> List[schemas.GetComment]:
    return service.get_comments(blog_id, include_all, author_id)

@router.put('/{comment_id}', status_code=status.HTTP_202_ACCEPTED)
def update_comment(comment_id: int, request: schemas.CommentUpdate, service: CommentService = Depends(get_comment_service(True))) -> schemas.CommentUpdate:
    return service.update_comment(comment_id, request)

@router.delete('/{comment_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_comment(comment_id: int, service: CommentService = Depends(get_comment_service(True))):
    return service.delete_comment(comment_id)