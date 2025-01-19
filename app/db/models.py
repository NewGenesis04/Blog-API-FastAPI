from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False, default= 'reader')
    blogs = relationship("Blog", back_populates="author")
    followers = relationship("Follow", foreign_keys="[Follow.followed_id]", back_populates="followed")
    following = relationship("Follow", foreign_keys="[Follow.follower_id]", back_populates="follower")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.username}, email='{self.email}, role={self.role}')>"


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, index=True,
                        default=lambda: datetime.now(timezone.utc))
    published_at = Column(DateTime, index=True, default=None)
    published = Column(Boolean, index=True, default=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="blogs")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title})>"
    

class Follow(Base):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, index=True,
                        default=lambda: datetime.now(timezone.utc))
    
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
    

    def __repr__(self):
        return f"<Follow(id={self.id}, follower_id={self.follower_id}, followed_id={self.followed_id})>"

