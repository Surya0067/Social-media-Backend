from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.db import Base

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('user.id')) 
    receiver_id = Column(Integer, ForeignKey('user.id')) 
    message = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="chats_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="chats_received")
