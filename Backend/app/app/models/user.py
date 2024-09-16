from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.db import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), index=True)
    phone_number = Column(String(10), nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_verfied = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    secret_key = Column(String(64),nullable=True)


    about = relationship("About", back_populates="user", uselist=False)
    otp = relationship("OTP", back_populates="user", uselist=False)
    posts = relationship("Post", back_populates="user")
    like = relationship('Like', back_populates='user')
    comment = relationship('Comment', back_populates='user')
    chats_sent = relationship("Chat", foreign_keys="[Chat.sender_id]", back_populates="sender")
    chats_received = relationship("Chat", foreign_keys="[Chat.receiver_id]", back_populates="receiver")