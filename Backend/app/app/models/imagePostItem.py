from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base

class ImagePostItem(Base):
    __tablename__ = "image_post_item"
    image_id = Column(String(255), primary_key=True,autoincrement=False)  #add nullable flase
    post_id = Column(Integer, ForeignKey('post.id'))
    file_path = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True) #add Nullable flase

    post = relationship("Post", back_populates="imagepostitems")
