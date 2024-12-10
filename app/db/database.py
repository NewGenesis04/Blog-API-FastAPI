from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from app.config import settings


def get_db():  # Function to create database connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SQLALCHEMY_DATABASE_URI = settings.DATABASE_URI
print("Database URL is ", SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
