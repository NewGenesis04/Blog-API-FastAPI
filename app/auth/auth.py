from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils import filter_user
from app.db.database import get_db
from app.db.models import User
from app.db import schemas

from app.auth.auth_utils import hash_password, verify_password, create_access_token, get_current_user, authenticate_user

router = APIRouter(tags=['auth'])

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type":"bearer"}


@router.post('/register')
def register_user(request: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserSummary:
    existing_user = filter_user(db, User.email == request.email)
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        hashed_password = hash_password(request.password)
        new_user = User(username=request.username, email=request.email, role= request.role, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error creating new user")
    
@router.put('/update_password')
def update_password(request: schemas.AuthPasswordUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        if not verify_password(request.old_password, user.password):
            raise HTTPException(status_code=400, detail="Old password incorrect")

        user.password = hash_password(request.new_password)
        db.commit()
        return {"detail": "Password updated"}

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating password: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password")
    except Exception as e:
        db.rollback()
        print(f"Error updating password: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password")