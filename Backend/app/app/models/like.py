from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.db import Base

class Like(Base):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # ForeignKey reference
    post_id = Column(Integer, ForeignKey('post.id'))
    liked_time = Column(DateTime,default=func.now())

    # Correctly reference the 'User' class name with an uppercase 'User'
    user = relationship("User", back_populates="like")
    post = relationship("Post",back_populates="like")