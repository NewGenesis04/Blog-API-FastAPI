from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends, status
from app.db.models import User, Follow, Blog, Comment
from app.db import schemas
from typing import List, Optional
from app.db.database import get_db
from app.auth.auth_utils import get_current_user, role_required


class BaseService:
    def __init__(self, db: Session, current_user: Optional[schemas.User]):
        """
        Base service class to provide shared functionality for all services.

        Args:
            db (Session): SQLAlchemy database session.
            current_user (User): The currently authenticated user.
        """
        self.db = db
        self.current_user = current_user


class FollowService(BaseService):

    def follow_user(self, user_id: int):
        """
        Follow a user by their ID.

        Args:
            user_id (int): The ID of the user to follow.

        Returns:
            dict: A success message indicating the user has been followed.

        Raises:
            HTTPException: If the user does not exist or is already followed.
        """
        try:
            user_to_follow = self.db.query(User).filter(User.id == user_id).first()
            if not user_to_follow:
                raise HTTPException(status_code=404, detail="User not found")

            # Check if already following
            existing_follow = self.db.query(Follow).filter_by(
                follower_id=self.current_user.id, followed_id=user_id
            ).first()
            if existing_follow:
                raise HTTPException(status_code=400, detail="You are already following this user.")

            # Create new follow relationship
            new_follow = Follow(follower_id=self.current_user.id, followed_id=user_id)
            self.db.add(new_follow)
            self.db.commit()
            return {"detail": f"User with id({user_id}) has been followed"}

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error following user")

    def unfollow_user(self, user_id: int):
        """
        Unfollow a user by their ID.

        Args:
            user_id (int): The ID of the user to unfollow.

        Returns:
            dict: A success message indicating the user has been unfollowed.

        Raises:
            HTTPException: If the user does not exist or is not currently followed.
        """
        try:
            # Check if the user to unfollow exists
            user_to_unfollow = self.db.query(User).filter(User.id == user_id).first()
            if not user_to_unfollow:
                raise HTTPException(status_code=404, detail="User not found")

            # Check if following exists
            existing_follow = self.db.query(Follow).filter_by(
                follower_id=self.current_user.id, followed_id=user_id
            ).first()
            if not existing_follow:
                raise HTTPException(status_code=400, detail="You are not following this user.")

            # Delete follow relationship
            self.db.delete(existing_follow)
            self.db.commit()
            return {"detail": f"User with id({user_id}) has been unfollowed"}

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error unfollowing user")
    
    def get_following(self, alt_user: Optional[int] = None) -> List[schemas.UserSummary]:
        """
        Get the list of users the current user or another user is following.

        Args:
            alt_user (Optional[int]): The ID of the user to check. Defaults to the current user.

        Returns:
            List[schemas.UserSummary]: A list of users being followed.

        Raises:
            HTTPException: If an error occurs while retrieving the data.
        """
        try:
            if alt_user:
                following = self.db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == alt_user).all()
            else:
                following = self.db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == self.current_user.id).all()
            if not following:
                return []
            
            return following
        
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error getting following: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting following")
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error getting following: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting following")
    
    def get_followers(self, alt_user: Optional[int] = None) -> List[schemas.UserSummary]:
        """
        Get the list of followers for the current user or another user.

        Args:
            alt_user (Optional[int]): The ID of the user to check. Defaults to the current user.

        Returns:
            List[schemas.UserSummary]: A list of followers.

        Raises:
            HTTPException: If an error occurs while retrieving the data.
        """
        try:
            if alt_user:
                followers = self.db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == alt_user).all()
            else:
                followers = self.db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == self.current_user.id).all()
            if not followers:
                return []
            
            return followers
        
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error getting followers: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting followers")
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error getting followers: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting followers")


class UserService(BaseService):

    def get_users(self) -> List[schemas.UserSummary]:
        """
        Retrieve all users from the database.

        Returns:
            List[schemas.UserSummary]: A list of all users.

        Raises:
            HTTPException: If an error occurs while retrieving the data.
        """
        try:
            users = self.db.query(User).all()
            return users
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error deleting blog: {str(e)}")
            raise HTTPException(
            status_code=500, detail="Error fetching users")

    def get_user_by_id(self, altId: Optional[int] = None) -> schemas.User:
        """
        Retrieve a user by their ID.

        Args:
            altId (Optional[int]): The ID of the user to retrieve. Defaults to the current user.

        Returns:
            schemas.User: The user data.

        Raises:
            HTTPException: If the user does not exist or an error occurs.
        """
        try:
            if altId:
                user = self.db.query(User).filter(User.id == altId).first()
            else:
                user = self.current_user
            if not user:
                raise HTTPException(status_code=404, detail=f"User with id {altId} not found")
            return user
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error getting user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting user")
        
    def update_user(self, request: schemas.UserUpdate):
        """
        Update the current user's information.

        Args:
            request (schemas.UserUpdate): The updated user data.

        Returns:
            dict: A success message indicating the user has been updated.

        Raises:
            HTTPException: If the user does not exist or an error occurs.
        """
        try:
            user = self.db.query(User).filter(User.id == self.current_user.id).first()  
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            update_data = request.model_dump(exclude_unset=True)  # Exclude fields not provided
            for key, value in update_data.items():
                setattr(user, key, value) 
                
            self.db.commit()
            return {"detail": f"User with id({self.current_user.id}) has been updated"}
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error updating user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error updating user")
            
    def delete_user(self):
        """
        Delete the current user's account.

        Returns:
            dict: A success message indicating the user has been deleted.

        Raises:
            HTTPException: If the user does not exist or an error occurs.
        """
        try:
            self.db.delete(self.current_user)
            self.db.commit()
            return {"detail": f"User with name: {self.current_user.username} and id: {self.current_user.id} has been deleted"}
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error updating user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error deleting user")    
    
    
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
            author_id = self.current_user.id
            if self.current_user.role == 'admin':
                author_id = request.author_id or self.current_user.id #Use payload id if available in request else default to current user(admin)
                        
                author = self.db.query(User).filter(User.id == request.author_id).first()

                if not author:
                    raise HTTPException(
                    status_code=404,
                    detail=f"Author with id({request.author_id}) not found"
                    )
            
            new_blog = Blog(title=request.title,
                            content=request.content,
                            published=request.published,
                                tag=request.tag,
                                published_at=request.published_at,
                                    author_id=author_id)
            
            self.db.add(new_blog)
            self.db.commit()
            self.db.refresh(new_blog)
            return new_blog
        
        except SQLAlchemyError as e:
            print(f"Error creating blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error creating blog")
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error creating blog: {str(e)}")
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

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting blogs: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error retrieving blogs")
        except Exception as e:
            print(f"Error getting blogs: {str(e)}")
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
            blog = self.db.query(Blog).filter(Blog.author_id == self.current_user.id).all()
            if not blog:
                raise HTTPException(status_code=404, detail="No blogs found for this user")
            
            return blog
        
        except SQLAlchemyError as e:
            print(f"Error getting blog: {str(e)}")
            raise HTTPException(
                    status_code=500, detail="Error getting blog")
        except Exception as e:
            print(f"Error getting blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting blog")
            
    def get_blog_by_id(self, id: int):
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
                raise HTTPException(status_code=404, detail="Blog not found")
            if blog.published == False and blog.author_id != self.current_user.id and self.current_user.role != 'admin':
                raise HTTPException(status_code=403, detail="You do not have access to this blog")
            return blog
        except SQLAlchemyError as e:
            print(f"Error getting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting blog")
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error getting blog: {str(e)}")
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
                raise HTTPException(status_code=404, detail=f"Blog with id({id}) not found")
            if blog.author_id != self.current_user.id:
                raise HTTPException(status_code=403, detail="You are not authorized to update this blog")
            
            update_data = request.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(blog, key, value)

            self.db.commit()
            self.db.refresh(blog)
            return {"detail": f"Blog with id({id}) has been updated"}
        
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error updating blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error updating blog")
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error updating blog: {str(e)}")
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
            blog = self.db.query(Blog).filter(Blog.id ==  id).first()
            if not blog:
                raise HTTPException(status_code=404, detail="Blog not found")
            if self.current_user.role == 'author' and blog.author_id != self.current_user.id:
                raise HTTPException(status_code=403, detail="You are not authorized to delete this blog")
            
            self.db.delete(blog)
            self.db.commit()
            return {"detail": f"Blog with id({id}) deleted"}
        
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error deleting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error deleting blog")
        except HTTPException:
            # Without this the exceptions above were defaulting to the generic exception handler below
            raise
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting blog: {str(e)}")
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
                raise HTTPException(status_code=404, detail="No blogs found with this tag")

            return blogs
        except SQLAlchemyError as e:
            print(f"Error getting blog: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error getting blog")
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error getting blog: {str(e)}")
            raise HTTPException(status_code=500, detail="Error getting blog")


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

#TODO: Augment the remaining routes in user, follows, comment