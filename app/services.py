from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends, status
from app.db.models import User, Follow, Blog, Comment
from app.db import schemas
from typing import List, Optional
from app.db.database import get_db
from app.auth.auth_utils import get_current_user, role_required


class FollowService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def follow_user(self, user_id: int):
        try:
            user_to_follow = self.db.query(User).filter(User.id == user_id).first()
            if not user_to_follow:
                raise HTTPException(status_code=404, detail="User not found")

            # Check if already following
            existing_follow = self.db.query(Follow).filter_by(
                follower_id=self.current_user.id, followed_id=user_id
            ).first()
            if existing_follow:
                raise HTTPException(status_code=400, detail="You are already following this user.")

            # Create new follow relationship
            new_follow = Follow(follower_id=self.current_user.id, followed_id=user_id)
            self.db.add(new_follow)
            self.db.commit()
            return {"detail": f"User with id({user_id}) has been followed"}

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error following user")

    def unfollow_user(self, user_id: int):
        try:
            # Check if the user to unfollow exists
            user_to_unfollow = self.db.query(User).filter(User.id == user_id).first()
            if not user_to_unfollow:
                raise HTTPException(status_code=404, detail="User not found")

            # Check if following exists
            existing_follow = self.db.query(Follow).filter_by(
                follower_id=self.current_user.id, followed_id=user_id
            ).first()
            if not existing_follow:
                raise HTTPException(status_code=400, detail="You are not following this user.")

            # Delete follow relationship
            self.db.delete(existing_follow)
            self.db.commit()
            return {"detail": f"User with id({user_id}) has been unfollowed"}

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error unfollowing user")
    
    def get_following(self, alt_user: Optional[int] = None) -> List[schemas.UserSummary]:
            try:
                if alt_user:
                    following = self.db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == alt_user).all()
                else:
                    following = self.db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == self.current_user.id).all()
                if not following:
                    return []
                
                return following
            
            except SQLAlchemyError as e:
                self.db.rollback()
                print(f"Error getting following: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error getting following")
            except HTTPException:
                raise
            except Exception as e:
                self.db.rollback()
                print(f"Error getting following: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error getting following")
    
    def get_followers(self, alt_user: Optional[int] = None) -> List[schemas.UserSummary]:
            try:
                if alt_user:
                    followers = self.db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == alt_user).all()
                else:
                    followers = self.db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == self.current_user.id).all()
                if not followers:
                    return []
                
                return followers
            
            except SQLAlchemyError as e:
                self.db.rollback()
                print(f"Error getting followers: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error getting followers")
            except HTTPException:
                raise
            except Exception as e:
                self.db.rollback()
                print(f"Error getting followers: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error getting followers")


class UserService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    def get_users(self) -> List[schemas.UserSummary]: 
        try:
            users = self.db.query(User).all()
            return users
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error deleting blog: {str(e)}")
            raise HTTPException(
            status_code=500, detail="Error fetching users")

    def get_user_by_id(self, alt_id: Optional[int] = None) -> schemas.User:
        try:
            if alt_id:
                user = self.db.query(User).filter(User.id == alt_id).first()
            else:
                user = self.db.query(User).filter(User.id == self.current_user.id).first()
            if not user:
                raise HTTPException(status_code=404, detail=f"User with id {alt_id} not found")
            return user
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error getting user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting user")
        
    def update_user(self, request: schemas.UserUpdate):
            try:
                user = self.db.query(User).filter(User.id == self.current_user.id).first()  
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                
                update_data = request.model_dump(exclude_unset=True)  # Exclude fields not provided
                for key, value in update_data.items():
                    setattr(user, key, value) 
                    
                self.db.commit()
                return {"detail": f"User with id({self.current_user.id}) has been updated"}
            except (SQLAlchemyError, Exception) as e:
                self.db.rollback()
                print(f"Error updating user: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error updating user")
            
    def delete_user(self):
        try:
            self.db.delete(self.current_user)
            self.db.commit()
            return {"detail": f"User with name: {self.current_user.username} and id: {self.current_user.id} has been deleted"}
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error updating user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error deleting user")    
    

class BlogService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user
    
