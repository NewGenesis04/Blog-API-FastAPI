import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.db.models import User, Blog, BlogLike
from app.db import schemas
from typing import List, Optional

from app.services.base_service import BaseService

# Initialize logger
logger = logging.getLogger(__name__)

class BlogService(BaseService):

    def create_blog(self, request: schemas.BlogCreate) -> schemas.Blog:
        """
        Create a new blog post.

        Args:
            request (schemas.BlogCreate): The blog data to create.

        Returns:
            schemas.Blog: The created blog post.

        Raises:
            HTTPException: If the author does not exist or an error occurs.
        """
        try:
            if self.current_user.role == 'admin':
                author_id = request.author_id or self.current_user.id
                author = self.db.query(User).filter(User.id == request.author_id).first()
                if not author:
                    logger.warning(f"Author with id({request.author_id}) not found")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Author with id({request.author_id}) not found"
                    )
            else:
                author_id = self.current_user.id

            new_blog = Blog(
                title=request.title,
                content=request.content,
                published=request.published,
                tag=request.tag,
                published_at=request.published_at,
                author_id=author_id
            )

            self.db.add(new_blog)
            self.db.commit()
            self.db.refresh(new_blog)
            logger.info(f"Blog created with id({new_blog.id}) by user({author_id})")
            return new_blog

        except SQLAlchemyError as e:
            logger.error(f"Error creating blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error creating blog")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error creating blog")

    def get_all_blogs(self, user_id: Optional[int] = None) -> List[schemas.Blog]:
        """
        Retrieve all blogs, optionally filtered by user ID.

        Args:
            user_id (Optional[int]): The ID of the user whose blogs to retrieve.

        Returns:
            List[schemas.Blog]: A list of blogs.

        Raises:
            HTTPException: If no blogs are found or an error occurs.
        """
        try:
            query = self.db.query(Blog)

            if self.current_user is None:
                # Unauthenticated users see only published blogs
                query = query.filter(Blog.published == True)

            elif self.current_user.role == "admin":
                # Admins can see everything, optionally filtered by author
                if user_id:
                    query = query.filter(Blog.author_id == user_id)

            else:
                # Regular authenticated users see only published blogs
                query = query.filter(Blog.published == True)
                if user_id:
                    query = query.filter(Blog.author_id == user_id)

            blogs = query.all()

            if not blogs:
                logger.warning("No blogs found")
                raise HTTPException(status_code=404, detail="Blogs not found")
            
            return [
                schemas.Blog(
                    **{k: v for k, v in blog.__dict__.items() if not k.startswith('_')},
                    like_count=len(blog.likes) if hasattr(blog,'likes') and blog.likes else 0,
                    comment_count=len(blog.comments) if hasattr(blog, 'comments') and blog.comments else 0,
                )
                for blog in blogs
            ]

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error getting blogs: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error retrieving blogs")
        except Exception as e:
            logger.error(f"Error getting blogs: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving blogs")

    def get_current_user_blogs(self) -> List[schemas.Blog]:
        """
        Retrieve all blogs authored by the current user.

        Returns:
            List[schemas.Blog]: A list of blogs authored by the current user.

        Raises:
            HTTPException: If no blogs are found or an error occurs.
        """
        try:
            blogs = self.db.query(Blog).filter(Blog.author_id == self.current_user.id).all()
            if not blogs:
                logger.warning(f"No blogs found for user {self.current_user.id}")
                raise HTTPException(status_code=404, detail="No blogs found for this user")

            return [
                schemas.Blog(
                    **{k: v for k, v in blog.__dict__.items() if not k.startswith('_')},
                    like_count=len(blog.likes) if hasattr(blog, 'likes') and blog.likes else 0,
                    comment_count=len(blog.comments) if hasattr(blog, 'comments') and blog.comments else 0,
                )
                for blog in blogs
            ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting blog")
        except Exception as e:
            logger.error(f"Error getting blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting blog")

    def get_blog_by_id(self, id: int) -> schemas.Blog:
        """
        Retrieve a blog by its ID.

        Args:
            id (int): The ID of the blog to retrieve.

        Returns:
            schemas.Blog: The blog data.

        Raises:
            HTTPException: If the blog does not exist or the user is not authorized to view it.
        """
        try:
            blog = self.db.query(Blog).filter(Blog.id == id).first()
            if not blog:
                logger.warning(f"Blog with id({id}) not found")
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.published == False and blog.author_id != self.current_user.id and self.current_user.role != 'admin':
                logger.warning(f"Unauthorized access to unpublished blog {id} by user {self.current_user.id}")
                raise HTTPException(status_code=403, detail="You do not have access to this blog")
            logger.info(f"Blog with id({id}) retrieved by user {self.current_user.id}")
            return schemas.Blog(
                **blog.__dict__,
                like_count=len(blog.likes) if blog.likes else 0,
                comment_count=len(blog.comments) if blog.comments else 0
            )
        
        except SQLAlchemyError as e:
            logger.error(f"Error getting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting blog")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting blog")

    def update_blog(self, request: schemas.BlogUpdate, id: int):
        """
        Update a blog post by its ID.

        Args:
            request (schemas.BlogUpdate): The updated blog data.
            id (int): The ID of the blog to update.
        
        Returns:
            dict: A success message indicating the blog has been updated.

        Raises:
            HTTPException: If the blog does not exist or the user is not authorized to update it.
        """
        try:
            blog = self.db.query(Blog).filter(Blog.id == id).first()

            if not blog:
                logger.warning(f"Blog with id({id}) not found for update")
                raise HTTPException(status_code=404, detail=f"Blog with id({id}) not found")
            if blog.author_id != self.current_user.id:
                logger.warning(f"User {self.current_user.id} not authorized to update blog {id}")
                raise HTTPException(status_code=403, detail="You are not authorized to update this blog")

            update_data = request.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(blog, key, value)

            self.db.commit()
            self.db.refresh(blog)
            logger.info(f"Blog with id({id}) updated by user {self.current_user.id}")
            return {"detail": f"Blog with id({id}) has been updated"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error updating blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error updating blog")
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error updating blog")

    def delete_blog(self, id: int):
        """
        Delete a blog post by its ID.

        Args:
            id (int): The ID of the blog to delete.

        Returns:
            dict: A success message indicating the blog has been deleted.

        Raises:
            HTTPException: If the blog does not exist or the user is not authorized to delete it.
        """
        try:
            blog = self.db.query(Blog).filter(Blog.id == id).first()
            if not blog:
                logger.warning(f"Blog with id({id}) not found for delete")
                raise HTTPException(status_code=404, detail="Blog not found")
            if self.current_user.role == 'author' and blog.author_id != self.current_user.id:
                logger.warning(f"User {self.current_user.id} not authorized to delete blog {id}")
                raise HTTPException(status_code=403, detail="You are not authorized to delete this blog")

            self.db.delete(blog)
            self.db.commit()
            logger.info(f"Blog with id({id}) deleted by user {self.current_user.id}")
            return {"detail": f"Blog with id({id}) deleted"}

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error deleting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error deleting blog")
        except HTTPException:
            # Without this the exceptions above were defaulting to the generic exception handler below
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error deleting blog")
        
    def sort_by_tag(self, tag:str) -> List[schemas.BlogSummary]:
        """
        Retrieve blogs filtered by a specific tag.

        Args:
            tag (str): The tag to filter blogs by.

        Returns:
            List[schemas.BlogSummary]: A list of blogs with the specified tag.

        Raises:
            HTTPException: If no blogs are found or an error occurs.
        """
        try:
            query = self.db.query(Blog).filter(Blog.tag == tag)

            if self.current_user.role != 'admin':  # Normal users should see only published blogs
                query = query.filter(Blog.published == True)

            blogs = query.all()

            if not blogs:
                logger.warning(f"No blogs found with tag: {tag}")
                raise HTTPException(status_code=404, detail="No blogs found with this tag")

            return blogs
        except SQLAlchemyError as e:
            logger.error(f"Error getting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting blog")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting blog")
        

    def like_blog(self, blog_id: int) -> dict:
        """
        """
        blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            logger.warning(f"Blog not found for like: {blog_id}")
            raise HTTPException(status_code=404, detail="Blog not found")
        
        existing_like = self.db.query(BlogLike).filter(
            BlogLike.blog_id == blog_id,
            BlogLike.user_id == self.current_user.id
        ).first()
        if existing_like:
            logger.info(f"User {self.current_user.id} already liked blog {blog_id}")
            raise HTTPException(status_code=400, detail="You have already liked this blog")
        new_like = BlogLike(blog_id=blog_id, user_id=self.current_user.id)
        self.db.add(new_like)
        self.db.commit()
        logger.info(f"User {self.current_user.id} liked blog {blog_id}")
        return {"detail": f"Blog with id({blog_id}) has been liked"}
    
    def unlike_blog(self, blog_id: int) -> dict:
        """
        """
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                logger.warning(f"Blog not found for unlike: {blog_id}")
                raise HTTPException(status_code=404, detail="Blog not found")
            
            existing_like = self.db.query(BlogLike).filter(
                BlogLike.blog_id == blog_id,
                BlogLike.user_id == self.current_user.id
            ).first()
            if not existing_like:
                logger.info(f"User {self.current_user.id} has not liked blog {blog_id}")
                raise HTTPException(status_code=400, detail="You have not liked this blog")
            
            self.db.delete(existing_like)
            self.db.commit()
            logger.info(f"User {self.current_user.id} unliked blog {blog_id}")
            return {"detail": f"Blog with id({blog_id}) has been unliked"}
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error unliking blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error unliking blog")