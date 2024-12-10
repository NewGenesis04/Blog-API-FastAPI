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
    blogs = relationship("Blog", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}')>"


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, index=True,
                        default=lambda: datetime.now(timezone.utc))
    published_at = Column(DateTime, index=True, default=None)
    published = Column(Boolean, index=True, default=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="blogs")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title})>"
