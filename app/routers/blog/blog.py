from fastapi import APIRouter, Query, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.db.models import Blog, User
from app.db.database import engine, get_db
from app.db import schemas
from app.utils import filter_blog
from app.auth.auth import router as auth_router
from app.auth.auth_utils import get_current_user, verify_access_token, role_required

router = APIRouter(dependencies= [Depends(get_current_user)], tags=['blog'])


# Blog CRUD Routes
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogCreate, user: User = Depends(role_required(['admin', 'author'])), db: Session = Depends(get_db)) -> schemas.Blog:
    try:
        new_blog = Blog(title=request.title, content=request.content, author_id=user.id)
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


@router.get('/', status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(['admin', 'author']))])
def get_all_blogs(db: Session = Depends(get_db), user_id: int = Query(None, description="Filter blogs by user ID")) -> List[schemas.Blog]:
    try:
        if user_id: blogs = db.query(Blog).filter(Blog.author_id == user_id).all()
        else:
            blogs = db.query(Blog).all()
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

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Blog, dependencies=[Depends(role_required(['author']))])
# The response_model can be used instead of declaring the output in the -> of the function.
# That is a cleaner method by the way. Using -> instead of declaring the response_model
def get_blog_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    # filter_blog returns db.query(models.Blog).filter(filter_condition)
    try:
        blog = filter_blog(db, Blog.id == id).first()
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


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_blog(request: schemas.BlogUpdate, id: int, user: User = Depends(role_required(['author'])), db: Session = Depends(get_db)):
    try:
        blog = filter_blog(db, Blog.id == id).first()
        if not blog:
            raise HTTPException(status_code=404, detail=f"Blog with id({id}) not found")

        #TODO: Create a way to validate that the blog being updated is for the authenticated user

        blog.title = request.title
        blog.content = request.content
        blog.published = request.published
        blog.author_id = user.id

        db.commit()
        return {"detail": f"Blog with id({id}) has been updated"}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error updating blog")
    except Exception as e:
        db.rollback()
        print(f"Error updating blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error updating blog")


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(role_required(['admin', 'author']))])
def delete_blog(id: int, db: Session = Depends(get_db)):
    try:
        #TODO: Create a way to validate that the blog being deleted is for the authenticated user
        row = filter_blog(db, Blog.id == id).first()
        if not row:
            raise HTTPException(status_code=404, detail="Blog not found")
        db.delete(row)
        db.commit()
        return {"detail": f"Blog with id({id}) deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error deleting blog")
    except Exception as e:
        db.rollback()
        print(f"Error deleting blog: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error deleting blog")