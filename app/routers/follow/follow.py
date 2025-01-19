from fastapi import APIRouter, Query, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.db.models import Blog, User
from app.db.database import get_db
from app.db import schemas