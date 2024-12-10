from app.db.models import Blog, User
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression
from app.db.database import engine, SessionLocal, get_db
from app.db import models

models.Base.metadata.create_all(bind=engine)


# Custom functions to reuse filter (Makes my life a little bit easier)

def filter_blog(db: Session, filter_condition: BinaryExpression):
    return db.query(models.Blog).filter(filter_condition)


def filter_user(db: Session, filter_condition: BinaryExpression):
    return db.query(models.User).filter(filter_condition)
