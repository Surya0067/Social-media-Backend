from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.db import Base

class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))  
    otp = Column(Integer, nullable=False)
    expired_time = Column(DateTime)

    user = relationship("User", back_populates="otp")