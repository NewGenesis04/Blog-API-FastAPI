from typing import Annotated, Optional
from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from app.auth.auth_utils import get_current_user
from app.db import schemas
from app.db.database import get_db
from app.services.follow_service import FollowService


def get_follow_service(require_user: bool = False):
    """Factory to enforce (or skip) auth dynamically per route."""
    def _get_service(                                                
        db: Session = Depends(get_db),
        current_user: Optional[schemas.User] = Depends(get_current_user) if require_user else None,
    ):
        if require_user and current_user is None:
            raise HTTPException(401, "Authentication required")
        return FollowService(db, current_user)
    return _get_service


FollowServiceDependency = Annotated[FollowService, Depends(get_follow_service)]
