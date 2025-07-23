from sqlalchemy.orm import Session
from app.db import schemas
from typing import Optional


class BaseService:
    def __init__(self, db: Session, current_user: Optional[schemas.User]):
        """
        Base service class to provide shared functionality for all services.

        Args:
            db (Session): SQLAlchemy database session.
            current_user (User): The currently authenticated user.
        """
        self.db = db
        self.current_user = current_user
        