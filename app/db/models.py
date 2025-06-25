from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    job_description = Column(String(255), nullable=True)
    profile_url = Column(String(255), nullable=True)
    cover_photo_url = Column(String(255), nullable=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    bio = Column(Text, nullable=True)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False, server_default='reader')
    blogs = relationship("Blog", back_populates="author")
    followers = relationship("Follow", foreign_keys="[Follow.followed_id]", back_populates="followed")
    following = relationship("Follow", foreign_keys="[Follow.follower_id]", back_populates="follower")
    comments = relationship("Comment", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.username}, email='{self.email}, role={self.role}')>"


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tag = Column(String(255), index=True, nullable=True) 
    created_at = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    likes = Column(Integer, nullable=False, default=0, server_default='0', index=True)    
    published_at = Column(DateTime, index=True, default=None)
    published = Column(Boolean, index=True, default=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    likes = relationship("BlogLike", back_populates="blog")
    author = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title})>"
    
class BlogLike(Base):
    __tablename__ = 'blog_likes'
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    created_at = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    blog = relationship("Blog", back_populates="likes")
    user = relationship("User")

    def __repr__(self):
        return f"<CommentLike(id={self.id}, blog_id={self.blog_id}, user_id={self.user_id})>"


class Follow(Base):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")

    def __repr__(self):
        return f"<Follow(id={self.id}, follower_id={self.follower_id}, followed_id={self.followed_id})>"

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'), index=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False, index=True)
    content = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False, default=0, server_default='0', index=True)
    created_at = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    likes = relationship("CommentLike", back_populates="comment")
    blog = relationship("Blog", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, author_id={self.author_id}, content={self.content})>"
    
class CommentLike(Base):
    __tablename__ = 'comment_likes'
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    created_at = Column(DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    comment = relationship("Comment", back_populates="likes")
    user = relationship("User")

    def __repr__(self):
        return f"<CommentLike(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id})>"
    
class RevokedToken(Base):
    __tablename__= 'revoked_tokens'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), nullable=False, index=True, unique=True)
    expires = Column(DateTime, nullable=False)