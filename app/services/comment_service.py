import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.models import Comment, Blog
from app.db import schemas
from typing import Optional

from app.services.base_service import BaseService

# Initialize logger
logger = logging.getLogger(__name__)

class CommentService(BaseService):
    
    def comment_on_blog(self, request: schemas.CreateComment, blog_id) -> schemas.CreateComment:
        """
        Add a comment to a blog post.

        Args:
            request (schemas.CreateComment): The comment data.
            blog_id (int): The ID of the blog to comment on.

        Returns:
            schemas.CreateComment: The created comment.

        Raises:
            HTTPException: If the blog does not exist or an error occurs.
        """
        try:
            
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                raise HTTPException(
                    status_code=404, detail="Blog not found")
            
            new_comment = Comment(author_id=self.current_user.id, blog_id=blog_id, content= request.content)

            self.db.add(new_comment)
            self.db.commit()
            self.db.refresh(new_comment)

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
    
    def get_comments(self, author_id: int, blog_id: int, include_all: Optional[bool] = None):
        """
        Retrieve comments for a blog post.

        Args:
            author_id (int): The ID of the comment author.
            blog_id (int): The ID of the blog.
            include_all (Optional[bool]): Whether to include all comments.

        Returns:
            List[schemas.Comment]: A list of comments.

        Raises:
            HTTPException: If no comments are found or an error occurs.
        """
        try:
            if author_id:
                comments = self.db.query(Comment).filter(Comment.blog_id == blog_id, Comment.author_id == author_id).all()
            elif include_all is True:
                comments = self.db.query(Comment).filter(Comment.blog_id == blog_id).all()
            else:
                comments = self.db.query(Comment).filter(Comment.blog_id == blog_id, Comment.author_id == self.current_user.id).all()
            
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
            
    def update_comment(self, request: schemas.CommentUpdate, comment_id)  -> schemas.CommentUpdate:
        """
        Update a comment by its ID.

        Args:
            request (schemas.CommentUpdate): The updated comment data.
            comment_id (int): The ID of the comment to update.

        Returns:
            schemas.CommentUpdate: The updated comment.

        Raises:
            HTTPException: If the comment does not exist or the user is not authorized to update it.
        """
        try:
            comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                raise HTTPException(status_code=404, detail="No comment found")
            if comment.author_id != self.current_user.id:
                raise HTTPException(status_code=403, detail="You are not authorized to update this comment")
            
            comment.content = request.content
            self.db.commit()
            self.db.refresh(comment)
            return comment
        
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error updating comments: {str(e)}")
            raise HTTPException(status_code=500, detail="Error updating comment")
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error updating comments: {str(e)}")
            raise HTTPException(status_code=500, detail="Error updating comment")
    
    def delete_comment(self, comment_id: int):
        """
        Delete a comment by its ID.

        Args:
            comment_id (int): The ID of the comment to delete.

        Returns:
            dict: A success message indicating the comment has been deleted.

        Raises:
            HTTPException: If the comment does not exist or the user is not authorized to delete it.
        """
        try:
            comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
            if comment.author_id != self.current_user.id:
                raise HTTPException(status_code=403, detail="You are not authorized to delete this comment")
            
            self.db.delete(comment)
            self.db.commit()

            return {"detail": f"Comment with id({comment_id}) has been deleted"}
        
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error deleting comment: {str(e)}")
            raise HTTPException(status_code=500, detail="Error deleting comment")
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting comment: {str(e)}")
            raise HTTPException(status_code=500, detail="Error deleting comment")