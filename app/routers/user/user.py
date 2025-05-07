from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user, role_required
from fastapi import APIRouter
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)


def get_user_service(require_user: bool = False):
    """Factory to enforce (or skip) auth dynamically per route."""
    def _get_service(                                                
        db: Session = Depends(get_db),
        current_user: Optional[schemas.User] = Depends(get_current_user) if require_user else None,
    ):
        if require_user and current_user is None:
            raise HTTPException(401, "Authentication required")
        return UserService(db, current_user)
    return _get_service

router = APIRouter(dependencies=[Depends(get_current_user)], tags=['user'])


@router.get('/all', status_code=status.HTTP_200_OK) 
def get_users(service: UserService = Depends(get_user_service(False))) -> List[schemas.UserSummary]:
    return service.get_users()

@router.get('/current', status_code=status.HTTP_200_OK)
def get_user_by_id(altId : Optional[int] = None, service: UserService = Depends(get_user_service(True))) -> schemas.User:
    return service.get_user_by_id(altId)

@router.put('/update', status_code=status.HTTP_200_OK)
def update_user(request: schemas.UserUpdate, service: UserService = Depends(get_user_service(True))):
    return service.update_user(request)
    
@router.delete('/delete', status_code=status.HTTP_202_ACCEPTED)
def delete_user(service: UserService = Depends(get_user_service(True))):
    return service.delete_user()
