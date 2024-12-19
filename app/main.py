from fastapi import FastAPI, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.db.models import Blog, User
from app.db.database import engine, get_db
from app.db import schemas, models
from app.utils import filter_blog, filter_user
from app.auth.auth import router as auth_router
from app.routers.blog.blog import router as blog_router
from app.routers.user.user import router as user_router
from app.auth.auth_utils import get_current_user, verify_access_token


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(blog_router, prefix="/blog", tags=["blog"])
app.include_router(user_router, prefix="/user", tags=["user"])


