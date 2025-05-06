from venv import logger
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.db.models import User, Follow
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user, role_required
from app.services import FollowService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['follow'])

def get_follow_service(require_user: bool = False):
    """Factory to enforce (or skip) auth dynamically per route."""
    def _get_service(                                                
        db: Session = Depends(get_db),
        current_user: Optional[schemas.User] = Depends(get_current_user) if require_user else None,
    ):
        if require_user and current_user is None:
            raise HTTPException(401, "Authentication required")
        return FollowService(db, current_user)
    return _get_service

@router.post('/{userId}', status_code=status.HTTP_201_CREATED)
def follow_user(userId: int, service: FollowService = Depends(get_follow_service(True))):
    logger.info(f"follow_user endpoint has been called")
    return service.follow_user(userId)

@router.delete('/{userId}', status_code=status.HTTP_202_ACCEPTED)
def unfollow(userId: int, service: FollowService = Depends(get_follow_service(True))):
    return service.unfollow_user(userId)


@router.get('/following', status_code=status.HTTP_200_OK)
def get_following(alt_user: Optional[int] = None, service: FollowService = Depends(get_follow_service(True))) -> List[schemas.UserSummary]:
    logger.info(f"get_following endpoint has been called")
    return service.get_following(alt_user)

@router.get('/followers', status_code=status.HTTP_200_OK)
def get_followers(alt_user: Optional[int] = None, service: FollowService = Depends(get_follow_service(True))) -> List[schemas.UserSummary]:
    return service.get_followers(alt_user)


# *, ALLOWS YOU TO LIST PARAMS IN ANY ORDER.... So query before default params: From tomi fast api (36:52)e.t.c