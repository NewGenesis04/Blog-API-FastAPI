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
from app.utils import upload_profile_picture
import cloudinary.uploader

router = APIRouter(dependencies=[Depends(get_current_user)], tags=['files'])

@router.post('/upload-profile-pic')
def upload_profile_pic(db: Session = Depends(get_db), user: User = Depends(get_current_user), file: UploadFile = File(...)):
    try:
        response = upload_profile_picture(user, file, db)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])

        return response
    
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error uploading image")
    
@router.delete('/delete-profile-pic')
def delete_profile_pic(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        if user.profile_url:
            public_id = user.profile_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)

            user.profile_url = None
            db.commit()
            db.refresh(user)
            return {"detail": "Profile picture deleted"}
        else:
            raise HTTPException(status_code=400, detail="User does not have a profile picture")
    except Exception as e:
        print(f"error: {e}")
        raise HTTPException(
            status_code=500, detail="Error deleting image")