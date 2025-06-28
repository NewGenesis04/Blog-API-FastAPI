from email.policy import HTTP
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user
from app.api_descriptions import COMMENT_LIKE, COMMENT_CREATE, COMMENT_DELETE, COMMENT_UPDATE, COMMENT_GET_ALL
from app.services.comment_service import CommentService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(dependencies= [Depends(get_current_user)])

def get_comment_service(require_user: bool = False):
    """
    Factory to enforce (or skip) auth dynamically per route.

    Magic: If `require_user=False` but a valid token is provided, 
    the user is still injected! This allows routes to work for both public and private use cases.    
    """
    def _get_service(                                                
        db: Session = Depends(get_db),
        current_user: Optional[schemas.User] = Depends(get_current_user) if require_user else None,
    ):
        if require_user and current_user is None:
            raise HTTPException(401, "Authentication required")
        return CommentService(db, current_user)
    return _get_service

@router.post('/{blog_id}', status_code=status.HTTP_201_CREATED, description=COMMENT_CREATE)
def comment_on_blog(blog_id: int, service: CommentService = Depends(get_comment_service(True))) -> schemas.CreateComment:
    logger.info(f"comment_on_blog endpoint has been called for blog_id: {blog_id}")
    return service.comment_on_blog(blog_id)

@router.get("/{blog_id}", status_code=status.HTTP_200_OK, description=COMMENT_GET_ALL)
def get_comments(blog_id: int, include_all: Optional[bool] = False, author_id: Optional[int] = None, service: CommentService = Depends(get_comment_service(False))) -> List[schemas.GetComment]:
    logger.info(f"get_comments endpoint has been called for blog_id: {blog_id}, include_all: {include_all}, author_id: {author_id}")
    return service.get_comments(blog_id, include_all, author_id)

@router.post('/like/{comment_id}', status_code=status.HTTP_202_ACCEPTED, description=COMMENT_LIKE)
def like_comment(comment_id: int, service: CommentService = Depends(get_comment_service(True))) -> dict:
    logger.info(f"like_comment endpoint has been called for comment_id: {comment_id}")
    return service.like_comment(comment_id)

@router.post('/unlike/{comment_id}', status_code=status.HTTP_202_ACCEPTED)
def unlike_comment(comment_id: int, service: CommentService = Depends(get_comment_service(True))) -> dict:
    logger.info(f"unlike_comment endpoint has been called for comment_id: {comment_id}")
    return service.unlike_comment(comment_id)

@router.put('/{comment_id}', status_code=status.HTTP_202_ACCEPTED, description=COMMENT_UPDATE)
def update_comment(comment_id: int, request: schemas.CommentUpdate, service: CommentService = Depends(get_comment_service(True))) -> schemas.CommentUpdate:
    logger.info(f"update_comment endpoint has been called for comment_id: {comment_id}")
    return service.update_comment(comment_id, request)

@router.delete('/{comment_id}', status_code=status.HTTP_202_ACCEPTED, description=COMMENT_DELETE)
def delete_comment(comment_id: int, service: CommentService = Depends(get_comment_service(True))):
    logger.info(f"delete_comment endpoint has been called for comment_id: {comment_id}")
    return service.delete_comment(comment_id)