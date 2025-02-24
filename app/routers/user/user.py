from fastapi import Depends, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models import Blog, User
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user, role_required
from fastapi import APIRouter
from app.services import UserService


def get_user_service(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return UserService(db, user)

router = APIRouter(dependencies=[Depends(get_current_user)], tags=['user'])


@router.get('/all', status_code=status.HTTP_200_OK) 
def get_users(service: UserService = Depends(get_user_service)) -> List[schemas.UserSummary]:
    return service.get_users()

@router.get('/current', status_code=status.HTTP_200_OK)
def get_user_by_id(altId : Optional[int] = None, service: UserService = Depends(get_user_service)) -> schemas.User:
    return service.get_user_by_id(altId)

@router.put('/update', status_code=status.HTTP_200_OK)
def update_user(request: schemas.UserUpdate, service: UserService = Depends(get_user_service)):
    return service.update_user(request)
    
@router.delete('/delete', status_code=status.HTTP_202_ACCEPTED)
def delete_user(service: UserService = Depends(get_user_service)):
    return service.delete_user()
