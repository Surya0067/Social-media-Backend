from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base

class ImagePostItem(Base):
    __tablename__ = "image_post_item"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    file_path = Column(String(255), nullable=False)
    image_id = Column(String(255), unique=True)  #add nullable flase
    is_active = Column(Boolean, default=True) #add Nullable flase

    post = relationship("Post", back_populates="imagepostitems")
