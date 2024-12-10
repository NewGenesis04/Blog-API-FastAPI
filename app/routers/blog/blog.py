from fastapi import APIRouter, FastAPI, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.db.models import Blog, User
from app.db.database import engine, get_db
from app.db import schemas, models
from app.utils import filter_blog, filter_user
from app.auth.auth import router as auth_router
from app.auth.auth_utils import get_current_user, verify_access_token

router = APIRouter(dependencies= [Depends(get_current_user)])


# Blog CRUD Routes
@router.post("/", status_code=status.HTTP_201_CREATED, tags=['blog'])
def create_blog(request: schemas.BlogCreate, db: Session = Depends(get_db)) -> schemas.BlogCreate:
    try:
        new_blog = models.Blog(title=request.title, content=request.content, author_id=request.author_id)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except SQLAlchemyError as e:
        print(f"Error creating blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error creating blog")
    except Exception as e:
        print(f"Error creating blog: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating blog")


@router.get('/', status_code=status.HTTP_200_OK, tags=['blog'])
def get_all_blogs(db: Session = Depends(get_db)) -> List[schemas.Blog]:
    try:
        blogs = db.query(models.Blog).all()
        if not blogs:
            raise HTTPException(
                status_code=404, detail="Blogs not found")  # Method 1
        return blogs
    except SQLAlchemyError as e:
        print(f"Error getting blogs: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error retrieving blogs")
    except Exception as e:
        print(f"Error getting blogs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving blogs")


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog, tags=['blog'])
# The response_model can be used instead of declaring the output in the -> of the function.
# That is a cleaner method by the way. Using -> instead of declaring the response_model
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    # filter_blog returns db.query(models.Blog).filter(filter_condition)
    try:
        blog = filter_blog(db, models.Blog.id == id).first()
        if not blog:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": f"Blog with id({id}) not found, error is: {status.HTTP_404_NOT_FOUND}"}
        return blog
    except SQLAlchemyError as e:
        print(f"Error getting blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error getting blog")
    except Exception as e:
        print(f"Error getting blog: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting blog")


@router.put('/{id}', status_code=status.HTTP_200_OK,  tags=['blog'])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    try:
        blog = filter_blog(db, models.Blog.id == id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        blog.title = request.title
        blog.content = request.content
        blog.published = request.published
        blog.author_id = request.author_id

        db.commit()
        return {"detail": f"Blog with id({id}) has been updated"}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error updating blog")
    except Exception as e:
        print(f"Error updating blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error updating blog")


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    try:
        row = filter_blog(db, models.Blog.id == id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Blog not found")
        row.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"Blog with id({id}) deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error deleting blog")
    except Exception as e:
        print(f"Error deleting blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error deleting blog")
