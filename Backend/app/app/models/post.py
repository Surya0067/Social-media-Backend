from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.db import Base

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    caption = Column(String(250), nullable=True)
    post_time = Column(DateTime, default=func.now(), nullable=False)
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean,default= True)

    user = relationship("User", back_populates="posts")
    imagepostitems = relationship('ImagePostItem', back_populates='post')
    like = relationship('Like', back_populates='post')
    comment = relationship('Comment', back_populates='post')