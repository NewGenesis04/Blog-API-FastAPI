from typing import Annotated, Optional
from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from app.auth.auth_utils import get_current_user
from app.db import schemas
from app.db.database import get_db
from app.services.follow_service import FollowService


def get_service_with_user(
    db: Session = Depends(get_db),
    current_user: Optional[schemas.User] = Depends(get_current_user),
) -> FollowService:
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return FollowService(db, current_user)


def get_service(db: Session = Depends(get_db)) -> FollowService:
    return FollowService(db, current_user=None)


FollowServiceWithUser = Annotated[FollowService, Depends(get_service_with_user)]
FollowServiceWithoutUser = Annotated[FollowService, Depends(get_service)]
