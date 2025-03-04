from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import User
from app.db.database import get_db
from app.db import schemas
from app.services import BlogService
from app.auth.auth_utils import get_current_user, role_required

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['blog'])

def get_blog_service(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return BlogService(db, user)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogCreate, service: BlogService = Depends(get_blog_service)) -> schemas.Blog:
    return service.create_blog(request)

@router.get('/', status_code=status.HTTP_200_OK)
def get_all_blogs(user_id: Optional[int] = None, service: BlogService = Depends(get_blog_service)) -> List[schemas.Blog]:
    return service.get_all_blogs(user_id)
  
    
@router.get('/current', status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(['admin', 'author']))])
def get_current_user_blogs(service: BlogService = Depends(get_blog_service)) -> List[schemas.Blog]:
    return service.get_current_user_blogs()


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog, dependencies=[Depends(role_required(['admin', 'author', 'reader']))])
def get_blog_by_id(id: int, service: BlogService = Depends(get_blog_service)):
    return service.get_blog_by_id(id)

@router.put('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(['author']))])
def update_blog(request: schemas.BlogUpdate, id: int, service: BlogService = Depends(get_blog_service)):
    return service.update_blog(request, id)


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(role_required(['admin', 'author']))])
def delete_blog(id: int, service: BlogService = Depends(get_blog_service)):
    return service.delete_blog(id)


@router.get('/tag/{tag}', status_code=status.HTTP_200_OK)
def sort_by_tag(tag: str, service: BlogService = Depends(get_blog_service)) -> List[schemas.BlogSummary]:
    return service.sort_by_tag(tag)
