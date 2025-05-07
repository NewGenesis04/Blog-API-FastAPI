import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.models import User, Follow
from app.db import schemas
from typing import List, Optional
from app.services.base_service import BaseService

# Initialize logger
logger = logging.getLogger(__name__)

class FollowService(BaseService):

    def follow_user(self, user_id: int):
        """
        Follow a user by their ID.

        Args:
            user_id (int): The ID of the user to follow.

        Returns:
            dict: A success message indicating the user has been followed.

        Raises:
            HTTPException: If the user does not exist or is already followed.
        """
        logger.info(f"Attempting to follow user with ID {user_id}")
        try:
            user_to_follow = self.db.query(User).filter(User.id == user_id).first()
            if not user_to_follow:
                logger.warning(f"User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")

            # Check if already following
            existing_follow = self.db.query(Follow).filter_by(
                follower_id=self.current_user.id, followed_id=user_id
            ).first()
            if existing_follow:
                logger.warning(f"User with ID {user_id} is already followed by user {self.current_user.id}")
                raise HTTPException(status_code=400, detail="You are already following this user.")

            # Create new follow relationship
            new_follow = Follow(follower_id=self.current_user.id, followed_id=user_id)
            self.db.add(new_follow)
            self.db.commit()
            logger.info(f"User with ID {user_id} successfully followed by user {self.current_user.id}")
            return {"detail": f"User with id({user_id}) has been followed"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error while following user with ID {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Error following user")

    def unfollow_user(self, user_id: int):
        """
        Unfollow a user by their ID.

        Args:
            user_id (int): The ID of the user to unfollow.

        Returns:
            dict: A success message indicating the user has been unfollowed.

        Raises:
            HTTPException: If the user does not exist or is not currently followed.
        """
        logger.info(f"Attempting to unfollow user with ID {user_id}")
        try:
            # Check if the user to unfollow exists
            user_to_unfollow = self.db.query(User).filter(User.id == user_id).first()
            if not user_to_unfollow:
                logger.warning(f"User with ID {user_id} not found")
                raise HTTPException(status_code=404, detail="User not found")

            # Check if following exists
            existing_follow = self.db.query(Follow).filter_by(
                follower_id=self.current_user.id, followed_id=user_id
            ).first()
            if not existing_follow:
                logger.warning(f"User with ID {user_id} is not currently followed by user {self.current_user.id}")
                raise HTTPException(status_code=400, detail="You are not following this user.")

            # Delete follow relationship
            self.db.delete(existing_follow)
            self.db.commit()
            logger.info(f"User with ID {user_id} successfully unfollowed by user {self.current_user.id}")
            return {"detail": f"User with id({user_id}) has been unfollowed"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error while unfollowing user with ID {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Error unfollowing user")
    
    def get_following(self, alt_user: Optional[int] = None) -> List[schemas.UserSummary]:
        """
        Get the list of users the current user or another user is following.

        Args:
            alt_user (Optional[int]): The ID of the user to check. Defaults to the current user.

        Returns:
            List[schemas.UserSummary]: A list of users being followed.

        Raises:
            HTTPException: If an error occurs while retrieving the data.
        """
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
        """
        Get the list of followers for the current user or another user.

        Args:
            alt_user (Optional[int]): The ID of the user to check. Defaults to the current user.

        Returns:
            List[schemas.UserSummary]: A list of followers.

        Raises:
            HTTPException: If an error occurs while retrieving the data.
        """
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