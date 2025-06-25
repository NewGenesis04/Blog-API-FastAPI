from app.db.models import User
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression
from app.db import models
from fastapi import UploadFile
import cloudinary.uploader

# Custom functions to reuse filter (Makes my life a little bit easier)

def filter_blog(db: Session, filter_condition: BinaryExpression):
    return db.query(models.Blog).filter(filter_condition)


def filter_user(db: Session, filter_condition: BinaryExpression):
    return db.query(models.User).filter(filter_condition)

def upload_profile_picture(user: User, file: UploadFile, db: Session):
    try:
        if user.profile_url:
            public_id = user.profile_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)


        upload_response = cloudinary.uploader.upload(file.file)
        img_url = upload_response["secure_url"]

        user.profile_url = img_url
        db.commit()
        db.refresh(user)

        return {"image_url": img_url}
    
    except Exception as e:
        return {"error": str(e)}
    
def upload_cover_photo(user: User, file: UploadFile, db: Session):
    try:
        if user.cover_photo_url:
            public_id = user.cover_photo_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)


        upload_response = cloudinary.uploader.upload(file.file)
        img_url = upload_response["secure_url"]

        user.cover_photo_url = img_url
        db.commit()
        db.refresh(user)

        return {"image_url": img_url}
    
    except Exception as e:
        return {"error": str(e)}
