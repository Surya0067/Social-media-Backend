from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.db import Base

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # ForeignKey reference
    post_id = Column(Integer, ForeignKey('post.id'))
    text = Column(String(255),nullable=True)
    commented_time = Column(DateTime,default=func.now())

    # Correctly reference the 'User' class name with an uppercase 'User'
    user = relationship("User", back_populates="comment")
    post = relationship("Post",back_populates="comment")