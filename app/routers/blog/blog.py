import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db import schemas
from app.services.blog_service import BlogService
from app.auth.auth_utils import get_current_user, role_required
import logging

logger = logging.getLogger(__name__)

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['blog'])

def get_blog_service(require_user: bool = False):
    """
    Factory to enforce (or skip) auth dynamically per route.

    Magic: If `require_user=False` but a valid token is provided, 
    the user is still injected! This allows routes to work for both public and private use cases.
    
    """
    def _get_service(                                                
        db: Session = Depends(get_db),
        current_user: Optional[schemas.User] = Depends(get_current_user) if require_user else None,
    ):
        if require_user and current_user is None:
            raise HTTPException(401, "Authentication required")
        return BlogService(db, current_user)  # Passes user=None if not required
    return _get_service

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required(['admin', 'author']))])
def create_blog(request: schemas.BlogCreate, service: BlogService = Depends(get_blog_service(True))) -> schemas.Blog:
    logger.info("create_blog endpoint has been called")
    return service.create_blog(request)

@router.get('/', status_code=status.HTTP_200_OK)
def get_all_blogs(user_id: Optional[int] = None, service: BlogService = Depends(get_blog_service(True))) -> List[schemas.Blog]:
    logger.info("get_all_blogs endpoint has been called")
    return service.get_all_blogs(user_id)
  
    
@router.get('/current', status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(['admin', 'author']))])
def get_current_user_blogs(service: BlogService = Depends(get_blog_service(True))) -> List[schemas.Blog]:
    logger.info("get_current_user_blogs endpoint has been called")
    return service.get_current_user_blogs()


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog)
def get_blog_by_id(id: int, service: BlogService = Depends(get_blog_service(True))):
    logger.info(f"get_blog_by_id endpoint has been called with id: {id}")
    return service.get_blog_by_id(id)

@router.put('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(['author']))])
def update_blog(request: schemas.BlogUpdate, id: int, service: BlogService = Depends(get_blog_service(True))):
    logger.info(f"update_blog endpoint has been called with id: {id}")
    return service.update_blog(request, id)


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(role_required(['admin', 'author']))])
def delete_blog(id: int, service: BlogService = Depends(get_blog_service(True))):
    logger.info(f"delete_blog endpoint has been called with id: {id}")
    return service.delete_blog(id)


@router.get('/tag/{tag}', status_code=status.HTTP_200_OK)
def sort_by_tag(tag: str, service: BlogService = Depends(get_blog_service(False))) -> List[schemas.BlogSummary]:
    logger.info(f"sort_by_tag endpoint has been called with tag: {tag}")
    return service.sort_by_tag(tag)
