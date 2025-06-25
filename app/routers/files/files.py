from urllib import response
from fastapi import HTTPException, Depends, status
from fastapi import APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.db.models import Blog, User
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user
from app.utils import upload_profile_picture, upload_cover_photo
from app.api_descriptions import FILE_GET_COVER_PHOTO, FILE_GET_PROFILE_PIC, FILE_UPLOAD_PROFILE_PIC, FILE_UPLOAD_COVER_PHOTO, FILE_DELETE_PROFILE_PIC, FILE_DELETE_COVER_PHOTO
import cloudinary.uploader

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post('/upload-profile-pic', description=FILE_UPLOAD_PROFILE_PIC)
def upload_profile_pic(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user), file: UploadFile = File(...)):
    try:
        user_model: User = db.query(User).filter(User.id == user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        response = upload_profile_picture(user_model, file, db)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])

        return response
    
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error uploading image")
    
@router.get('/profile-pic', description=FILE_GET_PROFILE_PIC)
def get_profile_pic(user: schemas.User = Depends(get_current_user)):
    try:
        if user.profile_url:
            return {"profile_url": user.profile_url}
        else:
            raise HTTPException(status_code=404, detail="User does not have a profile picture")
    except SQLAlchemyError as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error retrieving profile picture")
    
@router.get('/cover-photo', description=FILE_GET_COVER_PHOTO)
def get_cover_photo(user: schemas.User = Depends(get_current_user)):
    try:
        if user.cover_photo_url:
            return {"cover_photo_url": user.cover_photo_url}
        else:
            raise HTTPException(status_code=404, detail="User does not have a cover photo")
    except SQLAlchemyError as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error retrieving cover photo")
    
@router.post('/upload-cover-photo', description=FILE_UPLOAD_COVER_PHOTO )
def upload_cover_photo(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user), file: UploadFile = File(...)):
    try:
        user_model: User = db.query(User).filter(User.id == user.id).first()
        response = upload_cover_photo(user_model, file, db)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])

        return response
    
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error uploading cover photo")
    
@router.delete('/delete-profile-pic', description=FILE_DELETE_PROFILE_PIC)
def delete_profile_pic(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    try:
        # Check if user has a profile picture
        if user.profile_url:
            public_id = user.profile_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)
            user_model = db.query(User).filter(User.id == user.id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user_model.profile_url = None
            db.commit()
            db.refresh(user_model)
            return {"detail": "Profile picture deleted"}
        else:
            raise HTTPException(status_code=400, detail="User does not have a profile picture")
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error deleting image")

@router.delete('/delete-cover-photo', description=FILE_DELETE_COVER_PHOTO)
def delete_cover_photo(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    try:
        user_model: User = db.query(User).filter(User.id == user.id).first()
        if not user_model:
            raise HTTPException(status_code=404, detail="User not found")
        if user.cover_photo_url:
            public_id = user.cover_photo_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)

            user_model.cover_photo_url = None
            db.commit()
            db.refresh(user_model)
            return {"detail": "Profile picture deleted"}
        else:
            raise HTTPException(status_code=400, detail="User does not have a profile picture")
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error deleting image")
    