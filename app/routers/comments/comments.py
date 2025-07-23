from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.auth.auth_utils import get_current_user
from app.routers.comments.constants import (
    COMMENT_ON_BLOG_REQUEST_LOG,
    DELETE_COMMENT_REQUEST_LOG,
    GET_COMMENTS_REQUEST_LOG,
    LIKE_COMMENT_REQUEST_LOG,
    UNLIKE_COMMENT_REQUEST_LOG,
    UPDATE_COMMENT_REQUEST_LOG,
)
from app.routers.comments.dependencies import (
    CommentServiceWithUser,
    CommentServiceWithoutUser,
)
from app.routers.comments.descriptions import (
    COMMENT_CREATE,
    COMMENT_DELETE,
    COMMENT_GET_ALL,
    COMMENT_LIKE,
    COMMENT_UPDATE,
)
from app.routers.comments.schemas import CommentUpdate, GetComment
import logging

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "/{blog_id}",
    status_code=status.HTTP_201_CREATED,
    description=COMMENT_CREATE,
)
def comment_on_blog(
    blog_id: int, service: CommentServiceWithUser
):
    logger.info(COMMENT_ON_BLOG_REQUEST_LOG.format(blog_id=blog_id))
    return service.comment_on_blog(blog_id)


@router.get(
    "/{blog_id}",
    status_code=status.HTTP_200_OK,
    description=COMMENT_GET_ALL,
    response_model=List[GetComment],
)
def get_comments(
    service: CommentServiceWithoutUser,
    blog_id: int,
    include_all: Optional[bool] = False,
    author_id: Optional[int] = None,
):
    logger.info(
        GET_COMMENTS_REQUEST_LOG.format(
            blog_id=blog_id, author_id=author_id, include_all=include_all
        )
    )
    return service.get_comments(blog_id, include_all, author_id)


@router.post(
    "/like/{comment_id}",
    status_code=status.HTTP_202_ACCEPTED,
    description=COMMENT_LIKE,
)
def like_comment(
    comment_id: int, service: CommentServiceWithUser
) -> dict:
    logger.info(LIKE_COMMENT_REQUEST_LOG.format(comment_id=comment_id))
    return service.like_comment(comment_id)


@router.post(
    "/unlike/{comment_id}", status_code=status.HTTP_202_ACCEPTED
)
def unlike_comment(
    comment_id: int, service: CommentServiceWithUser
):
    """Unlike a comment by its ID."""
    logger.info(UNLIKE_COMMENT_REQUEST_LOG.format(comment_id=comment_id))
    return service.unlike_comment(comment_id)


@router.put(
    "/{comment_id}",
    status_code=status.HTTP_202_ACCEPTED,
    description=COMMENT_UPDATE,
    response_model=CommentUpdate,
)
def update_comment(
    comment_id: int, data: CommentUpdate, service: CommentServiceWithUser
):
    logger.info(UPDATE_COMMENT_REQUEST_LOG.format(comment_id=comment_id))
    return service.update_comment(comment_id, data)


@router.delete(
    "/{comment_id}", 
    status_code=status.HTTP_202_ACCEPTED, 
    description=COMMENT_DELETE
)
def delete_comment(
    comment_id: int, service: CommentServiceWithUser
):
    logger.info(DELETE_COMMENT_REQUEST_LOG.format(comment_id=comment_id))
    return service.delete_comment(comment_id)
