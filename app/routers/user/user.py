from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user
from app.api_descriptions import USER_GET_ALL, USER_UPDATE, USER_DELETE, USER_GET_CURRENT_USER
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

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get('/all', status_code=status.HTTP_200_OK, description=USER_GET_ALL) 
def get_users(service: UserService = Depends(get_user_service(False))) -> List[schemas.UserSummary]:
    logger.info("get_users endpoint has been called")
    return service.get_users()

@router.get('/current', status_code=status.HTTP_200_OK, description=USER_GET_CURRENT_USER)
def get_current_user(altId : Optional[int] = None, service: UserService = Depends(get_user_service(True))) -> schemas.User:
    logger.info("get_user_by_id endpoint has been called")
    return service.get_current_user(altId)

@router.put('/update', status_code=status.HTTP_200_OK, description=USER_UPDATE)
def update_user(request: schemas.UserUpdate, service: UserService = Depends(get_user_service(True))):
    logger.info("update_user endpoint has been called")
    return service.update_user(request)
    
@router.delete('/delete', status_code=status.HTTP_202_ACCEPTED, description=USER_DELETE)
def delete_user(service: UserService = Depends(get_user_service(True))):
    logger.info("delete_user endpoint has been called")
    return service.delete_user()
