from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.db.models import User, Follow
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user, role_required
from app.services import FollowService

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['follow'])

def get_follow_service(db: Session = Depends(get_db), user: User = Depends(role_required(['reader', 'author']))):
    return FollowService(db, user)

@router.post('/{userId}', status_code=status.HTTP_201_CREATED)
def follow_user(userId, service: FollowService = Depends(get_follow_service)):
    return service.follow_user(userId)

@router.delete('/{userId}', status_code=status.HTTP_202_ACCEPTED)
def unfollow(userId, service: FollowService = Depends(get_follow_service)):
    return service.unfollow_user(userId)


@router.get('/following', status_code=status.HTTP_200_OK)
def get_following(alt_user: Optional[int] = None, service: FollowService = Depends(get_follow_service)) -> List[schemas.UserSummary]:
    return service.get_following(alt_user)

    

@router.get('/followers', status_code=status.HTTP_200_OK)
def get_followers(alt_user: Optional[int] = None, service: FollowService = Depends(get_follow_service)) -> List[schemas.UserSummary]:
    return service.get_followers(alt_user)


# *, ALLOWS YOU TO LIST PARAMS IN ANY ORDER.... So query before default params: From tomi fast api (36:52)e.t.c