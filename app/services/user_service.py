import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.models import User
from app.db import schemas
from typing import List, Optional

from app.routers import user
from app.services.base_service import BaseService

# Initialize logger
logger = logging.getLogger(__name__)


class UserService(BaseService):

    def get_users(self) -> List[schemas.UserSummary]:
        """
        Retrieve all users from the database.

        Returns:
            List[schemas.UserSummary]: A list of all users.

        Raises:
            HTTPException: If an error occurs while retrieving the data.
        """
        try:
            users = self.db.query(User).all()
            return users
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error deleting blog: {str(e)}")
            raise HTTPException(
            status_code=500, detail="Error fetching users")

    def get_current_user(self, altId: Optional[int] = None) -> schemas.User:
        """
        Retrieve a user by their ID.

        Args:
            altId (Optional[int]): The ID of the user to retrieve. Defaults to the current user.

        Returns:
            schemas.User: The user data.

        Raises:
            HTTPException: If the user does not exist or an error occurs.
        """
        try:
            if altId:
                user = self.db.query(User).filter(User.id == altId).first()
            else:
                user = self.current_user
            if not user:
                raise HTTPException(status_code=404, detail=f"User with id {altId} not found")
            return user
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error getting user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting user")
        
    def update_user(self, request: schemas.UserUpdate):
        """
        Update the current user's information.

        Args:
            request (schemas.UserUpdate): The updated user data.

        Returns:
            dict: A success message indicating the user has been updated.

        Raises:
            HTTPException: If the user does not exist or an error occurs.
        """
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
        """
        Delete the current user's account.

        Returns:
            dict: A success message indicating the user has been deleted.

        Raises:
            HTTPException: If the user does not exist or an error occurs.
        """
        try:
            user = self.db.query(User).filter(User.id == self.current_user.id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            self.db.delete(user)
            self.db.commit()
            return {"detail": f"User with name: {self.current_user.username} and id: {self.current_user.id} has been deleted"}
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error updating user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error deleting user")    