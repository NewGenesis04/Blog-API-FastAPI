from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.utils import filter_user
from app.config import settings
from typing import List
from app.db import schemas
from app.db.database import get_db
from app.db.models import User, RevokedToken
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def authenticate_user(db: Session, identifier: str, password: str):
    user = db.query(User).filter((User.email == identifier) | (User.username == identifier)).first()
    if user is None or not verify_password(password, user.password):
        print("Authentication failed")
        return False
    return user

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def revoke_token(db, refresh_token: str =Depends(oauth2_scheme)) -> RevokedToken:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        
        # Check if already revoked
        if db.query(RevokedToken).filter(RevokedToken.token == refresh_token).first():
            raise HTTPException(status_code=400, detail="Token already revoked")
        
        # Revoke it
        return RevokedToken(token=refresh_token, expires_at=expires_at)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.User:
    try:
        payload = verify_access_token(token) 
        user_id: int = payload.get("sub")
        if not user_id:
            print("No user_id specified")
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(user_id)
        current_user = filter_user(db, User.id == user_id).first()
        if not current_user:
            print("No user found in database")
            raise HTTPException(status_code=401, detail="User not found")
        
        return schemas.User.model_validate(current_user)
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

def role_required(allowed_roles: List[str]):
    def role_check(user: schemas.User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have the required role(s). Allowed roles: {allowed_roles}",
            )
        return user
    return role_check