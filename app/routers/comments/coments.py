from email.policy import HTTP
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.db.models import User, Blog, Comment
from app.db.database import get_db
from app.db import schemas
from app.auth.auth_utils import get_current_user, role_required


router = APIRouter(dependencies= [Depends(get_current_user)], tags=['comments'])

@router.post('/{blogId}', status_code=status.HTTP_201_CREATED)
def comment_on_blog(blogId: int, request: schemas.CreateComment, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> schemas.CreateComment:
    try:
        author_id = user.id
        blog = db.query(Blog).filter(Blog.id == blogId).first()
        if not blog:
            raise HTTPException(
                status_code=404, detail="Blog not found")
        
        new_comment = Comment(author_id=author_id, blog_id=blogId, content= request.content)

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        return new_comment
    
    except SQLAlchemyError as e:
        print(f"Error creating comment: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error creating comment")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating comment: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error creating comment") 


@router.get("/{blogId}", status_code=status.HTTP_200_OK)
def get_comments(blogId: int, db: Session = Depends(get_db), include_all: Optional[bool] = False, author_id: Optional[int] = None, user: User = Depends(get_current_user)) -> List[schemas.GetComment]:
    try:
        if author_id:
            comments = db.query(Comment).filter(Comment.blog_id == blogId, Comment.author_id == author_id).all()
        elif include_all is True:
            comments = db.query(Comment).filter(Comment.blog_id == blogId).all()
        else:
            comments = db.query(Comment).filter(Comment.blog_id == blogId, Comment.author_id == user.id).all()

        
        if not comments:
            raise HTTPException(status_code=404, detail="No comments found")
        
        return comments
        
    except SQLAlchemyError as e:
        print(f"Error getting comments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting comments")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting comments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting comments")
    

@router.put('/{commentId}', status_code=status.HTTP_202_ACCEPTED)
def update_comment(commentId: int, request: schemas.CommentUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> schemas.CommentUpdate:
    try:
        comment = db.query(Comment).filter(Comment.id == commentId).first()
        if not comment:
            raise HTTPException(status_code=404, detail="No comment found")
        if comment.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this comment")
        
        comment.content = request.content
        db.commit()
        db.refresh(comment)
        return comment
    
    except SQLAlchemyError as e:
        print(f"Error updating comments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating comment")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating comments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating comment")


@router.delete('/{commentId}', status_code=status.HTTP_202_ACCEPTED)
def delete_comment(commentId: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        comment = db.query(Comment).filter(Comment.id == commentId).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.author_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this comment")
        
        db.delete(comment)
        db.commit()

        return {"detail": f"Comment with id({commentId}) has been deleted"}
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting comment: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting comment")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting comment: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting comment")