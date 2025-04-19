from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends, status
from app.db.models import User, Follow, Blog, Comment
from app.db import schemas
from typing import List, Optional
from app.db.database import get_db
from app.auth.auth_utils import get_current_user, role_required


class BaseService:
    def __init__(self, db: Session, current_user: Optional[User]):
        self.db = db
        self.current_user = current_user


class FollowService(BaseService):

    def follow_user(self, user_id: int):
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
        try:
            users = self.db.query(User).all()
            return users
        except (SQLAlchemyError, Exception) as e:
            self.db.rollback()
            print(f"Error deleting blog: {str(e)}")
            raise HTTPException(
            status_code=500, detail="Error fetching users")

    def get_user_by_id(self, altId: Optional[int] = None) -> schemas.User:
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
        try:
            query = self.db.query(Blog)

            if self.current_user is None:
                query = query.filter(Blog.published == True)

            elif self.current_user.role == "admin":
                if user_id:
                    query = query.filter(Blog.author_id == user_id)

            else:  #authenticated but not admin
                query = query.filter(Blog.published == True)
                if user_id:
                    query = query.filter(Blog.author_id == user_id)

            blogs = query.all()

            if not blogs:
                raise HTTPException(status_code=404, detail="Blogs not found")

            return blogs

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            print(f"Error getting blogs: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Error retrieving blogs")
        except Exception as e:
            print(f"Error getting blogs: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving blogs")

    def get_current_user_blogs(self):
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
            try:
                blog = self.db.query(Blog).filter(Blog.id == id).first()

                if self.current_user is None:
                    if blog.published:
                        return blog
                    else:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have access to this blog")
                    
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
            

#TODO: Complete the switch to unprotected/protected routes