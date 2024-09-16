from typing import Any, Dict, Optional, Union
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from curd.curd_user import get
from models import User, Chat


def get_chat(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    return chat


def createChat(db: Session, sender_id: int, receiver_id: int, message: str):
    receiver = get(db=db, user_id=receiver_id)
    if receiver.is_active == True:
        db.add(
            Chat(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message,
            )
        )
        db.commit()
        return dict(message="Message sented")
    raise HTTPException(status_code=404, detail="User not found")


def deleteChat(db: Session, user_id: int, chat_id: int):
    chat = get_chat(db=db, chat_id=chat_id)
    if chat:
        if chat.sender_id == user_id:
            chat.is_deleted = True
            db.commit()
            db.refresh(chat)
            return dict(message="Message Deleted")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="you can't delete the message",
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")


def updateChat(db: Session, user_id: int, chat_id: int, message: str):
    chat = get_chat(db=db, chat_id=chat_id)
    if chat:
        if chat.sender_id == user_id:
            chat.message = message
            db.commit()
            db.refresh(chat)
            return dict(message="Message Updated")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="you can't update the message",
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")


def getUserChatList(db: Session, current_user_id: int):
    sent_chats = (
        db.query(Chat)
        .filter(Chat.sender_id == current_user_id, Chat.is_deleted == False)
        .order_by(Chat.created_at.desc())
        .all()
    )
    received_chats = (
        db.query(Chat)
        .filter(Chat.receiver_id == current_user_id, Chat.is_deleted == False)
        .order_by(Chat.created_at.desc())
        .all()
    )

    chat_list = {}

    # Create a dict of last messages with each user
    for chat in sent_chats + received_chats:
        other_user_id = (
            chat.receiver_id if chat.sender_id == current_user_id else chat.sender_id
        )

        # Update only if it's the latest message for that user
        if (
            other_user_id not in chat_list
            or chat.created_at > chat_list[other_user_id]["created_at"]
        ):
            chat_list[other_user_id] = {
                "last_message": chat.message,
                "created_at": chat.created_at,
            }

    # Fetch user details for the chat list
    user_chat_list = []
    for other_user_id, chat_data in chat_list.items():
        user = db.query(User).filter(User.id == other_user_id).first()
        profile_image = (
            user.about.profile_photo
            if user.about and user.about.profile_photo
            else None
        )
        user_chat_list.append(
            {
                "user_id": user.id,
                "username": user.username,
                "profile_image": profile_image,
                "last_message": chat_data["last_message"],
                "created_at": chat_data["created_at"],
            }
        )

    return user_chat_list



def chatDisplay(db: Session, current_user_id: int, other_user_id: int):
    chat = db.query(Chat).filter(
        or_(
            (Chat.sender_id == current_user_id) & (Chat.receiver_id == other_user_id),
            (Chat.sender_id == other_user_id) & (Chat.receiver_id == current_user_id)
        ),Chat.is_deleted==False
    ).order_by(
        Chat.created_at.desc()
    ).all()

    if chat:
        return chat
    raise HTTPException(status_code=404,detail="Chat Not Found")