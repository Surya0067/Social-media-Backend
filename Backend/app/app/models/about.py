from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base

class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    account_status = Column(String(10), nullable=False, default="public")
    bio = Column(String(250), nullable=True)
    profile_photo = Column(String(255), nullable=True)
    updated_at = Column(DateTime, default=func.now())
    #foreign key
    user_id = Column(Integer, ForeignKey('user.id'))
    
    # Establish the relationship with the 'User' model
    user = relationship("User", back_populates="about")

