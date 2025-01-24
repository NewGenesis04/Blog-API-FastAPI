from fastapi import APIRouter, Query, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.db.models import User, Follow
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user, role_required

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['follow'])

@router.post('/{userId}', status_code=status.HTTP_201_CREATED)
def follow_user(userId, db: Session = Depends(get_db), user: User = Depends(role_required(['reader', 'author']))):
    try:
        user_to_follow = db.query(User).filter(User.id == userId).first()
        if not user_to_follow:
            raise HTTPException(
                status_code=404, detail="User not found")
        
        existing_follow = db.query(Follow).filter_by(follower_id=user.id, followed_id=userId).first()
        if existing_follow:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already following this user.")
        
        new_follow = Follow(follower_id=user.id, followed_id=userId)
        db.add(new_follow)
        db.commit()
        return {"detail": f"User with id({userId}) has been followed"}
    
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Erorr: {e}")
        raise HTTPException(status_code=500, detail="Error following user")
        

@router.delete('/{userId}', status_code=status.HTTP_202_ACCEPTED)
def unfollow(userId, db: Session = Depends(get_db), user: User = Depends(role_required(['reader', 'author']))):
    try:
        user_to_unfollow = db.query(User).filter(User.id == userId).first()
        if not user_to_unfollow:
            raise HTTPException(
                status_code=404, detail="User not found")
        
        existing_follow = db.query(Follow).filter_by(follower_id=user.id, followed_id=userId).first()
        if not existing_follow:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not following this user.")
        
        db.delete(existing_follow)
        db.commit()
        return {"detail": f"User with id({userId}) has been unfollowed"}
    
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Erorr: {e}")
        raise HTTPException(status_code=500, detail="Error unfollowing user")
    
@router.get('/following', status_code=status.HTTP_200_OK)
def get_following(alt_user: int = Query(None, description="Filter following by user ID"),db: Session = Depends(get_db), user: User = Depends(role_required(['reader', 'author']))) -> List[schemas.UserSummary]:
    try:
        if alt_user:
            following = db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == alt_user).all()
        else:
            following = db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user.id).all()
        if not following:
            raise HTTPException(
                status_code=404, detail="Following not found")
        
        return following
    
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error getting following: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error getting following")
    

@router.get('/followers', status_code=status.HTTP_200_OK)
def get_followers(alt_user: int = Query(None, description="Filter following by user ID"), db: Session = Depends(get_db), user: User = Depends(role_required(['reader', 'author']))) -> List[schemas.UserSummary]:
    try:
        if alt_user:
            followers = db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == alt_user).all()
        else:
            followers = db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == user.id).all()
        if not followers:
            raise HTTPException(
                status_code=404, detail="Following not found")
        
        return followers
    
    except (SQLAlchemyError, Exception) as e:
        db.rollback()
        print(f"Error getting followers: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error getting followers")
    
#TODO: Change the Query to use just Optional[datatype]