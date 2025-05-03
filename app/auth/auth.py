from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Header
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils import filter_user
from app.db.database import get_db
from app.db.models import User, RevokedToken
from app.db import schemas

from app.auth.auth_utils import hash_password, verify_access_token, verify_password, get_current_user
from app.auth.auth_utils import oauth2_scheme, create_token, authenticate_user, revoke_token

router = APIRouter(tags=['auth'])

# @router.post('/login')
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username/email or password")
#     access_token = create_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=5))
#     refresh_token = create_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=7))
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type":"bearer"}


@router.post('/login')
def login(request: schemas.AuthLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.identifier, request.password)
    if not user:
       raise HTTPException(status_code=400, detail="Incorrect username/email or password")
    access_token = create_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=5))
    refresh_token = create_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=7))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type":"bearer"}

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }

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
    
@router.post("/logout")
def logout(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Revoke it
        revoked = revoke_token(refresh_token=refresh_token, db=db)

        db.add(revoked)
        db.commit()
        return {"detail": "Refresh token revoked, user logged out succesfully"}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token already expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    
@router.post("/refresh")
def refresh_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        user = verify_access_token(token)

        if db.query(RevokedToken).filter(RevokedToken.token == token).first():
            raise HTTPException(status_code=401, detail="Refresh token revoked")
        
        access_token = create_token({"sub": str(user.get('sub'))}, timedelta(minutes=5))
        return {"access_token": access_token, "token_type": "bearer"}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    



#TODO: Implement cookie-based auth flow for tokens
    