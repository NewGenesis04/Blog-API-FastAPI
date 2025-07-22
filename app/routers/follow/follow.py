import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.db import schemas
from app.auth.auth_utils import get_current_user
from app.routers.follow.dependencies import FollowServiceWithUser

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post(
    "/{user_id}", status_code=status.HTTP_201_CREATED,
)
def follow_user(
    user_id: int, service: FollowServiceWithUser,
):
    logger.info("follow_user endpoint has been called")
    return service.follow_user(user_id)


@router.delete(
    "/{user_id}", status_code=status.HTTP_202_ACCEPTED,
)
def unfollow(
    user_id: int, service: FollowServiceWithUser,
):
    logger.info(f"unfollow_user endpoint has been called with userId: {user_id}")
    return service.unfollow_user(user_id)


@router.get(
    "/following",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.UserSummary],
)
def get_following(
    service: FollowServiceWithUser,
    alt_user: Optional[int] = None,
):
    logger.info("get_following endpoint has been called")
    return service.get_following(alt_user)


@router.get(
    "/followers",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.UserSummary],
)
def get_followers(
    service: FollowServiceWithUser,
    alt_user: Optional[int] = None,
):
    logger.info(f"get_followers endpoint has been called with alt_user: {alt_user}")
    return service.get_followers(alt_user)
