from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.auth_utils import get_current_user
from app.db.database import get_db
from app.services.comment_service import CommentService


def get_comment_service_with_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> CommentService:
    return CommentService(db, current_user=current_user)


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db, current_user=None)


CommentServiceWithoutUser = Annotated[CommentService, Depends(get_comment_service)]
CommentServiceWithUser = Annotated[
    CommentService, Depends(get_comment_service_with_user)
]
