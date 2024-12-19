from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils import filter_user
from app.config import settings
from app.db.database import get_db
from app.db.models import User
from app.db import schemas

from app.auth.auth_utils import hash_password, verify_password, create_access_token, get_current_user, authenticate_user

router = APIRouter()

@router.post('/login', tags=['auth'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type":"bearer"}


@router.post('/register', tags=['auth'])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserSummary:
    existing_user = filter_user(db, User.email == user.email)
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        hashed_password = hash_password(user.password)
        new_user = User(username=user.username, email=user.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error creating new user")