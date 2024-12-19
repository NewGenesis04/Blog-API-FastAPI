from gc import get_debug
from multiprocessing import synchronize
from fastapi import FastAPI, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.db.models import Blog, User
from app.db.database import get_db
from app.db import schemas, models
from app.utils import filter_user
from app.auth.auth_utils import get_current_user, verify_access_token
from fastapi import APIRouter


router = APIRouter(dependencies=[Depends(get_current_user)], tags=['user'])

@router.get('/all') 
def get_users(db: Session = Depends(get_db), ) -> List[schemas.User]:
    try:
        users = db.query(User).all()
        return users
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error deleting blog: {str(e)}")
        raise HTTPException(
           status_code=500, detail="Error fetching users")



@router.get('/current')
def get_user_by_id(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> schemas.User:
    try:
        id = user.id
        fetched_user = db.query(models.User).filter(models.User.id == id).first()
        if not fetched_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'User of id{id} not found')
        print(fetched_user)
        return fetched_user
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error deleting blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error fetching user")


@router.put('/update')
def update_user(request: schemas.UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        id = user.id
        current_user = filter_user(db, models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        current_user.username = request.username
        current_user.email = request.email
        db.commit()
        return {"detail": f"User with id({id}) has been updated"}
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error updating user")
    
@router.delete('/delete')
def delete_user(request: schemas.UserDelete, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        id = user.id
        current_user = filter_user(db, models.User.id == id).first()
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        current_user.delete(synchronize=False)
        db.commit()
        return {"detail": f"User with name: {current_user.username} and id: {id} has been deleted"}
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error deleting user")