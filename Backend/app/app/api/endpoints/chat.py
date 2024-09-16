from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form, status
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_user
from models import User, Post, ImagePostItem
from schemas import PostCreate, PostDisplay, ListPostDisplay,MessageResponse,ChatDetailResponse,ChatDisplayResponse,ChatItemResponse,ChatListResponse
from curd.chat import createChat, deleteChat, updateChat, getUserChatList, chatDisplay
from core.config import settings


router = APIRouter()

@router.post("/sent-message/{receiver_id}", 
    description="Send a new message to a specific user.",
    response_model=MessageResponse)
async def sentMessage(
    message: str,
    receiver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = createChat(
        db=db, sender_id=current_user.id, receiver_id=receiver_id, message=message
    )
    return chat


@router.patch("/update-message/{chat_id}", 
    description="Update an existing message in the chat.",
    response_model=MessageResponse)
async def updateMessage(
    chat_id: int,
    message : str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = updateChat(db=db, user_id=current_user.id, chat_id=chat_id, message=message)
    return chat


@router.post("/delete-message/{chat_id}", 
    description="Delete a message you have sent in the chat.",
    response_model=MessageResponse)
async def deleteMessage(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat = deleteChat(db=db, user_id=current_user.id, chat_id=chat_id)
    return chat


@router.get("/chat-list", 
    description="Get a list of users you have chatted with and the last message exchanged.",
    response_model=ChatListResponse)
async def getChatList(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    chat_list = getUserChatList(db=db, current_user_id=current_user.id)
    if chat_list:
        return {"chat_list": chat_list}
    raise HTTPException(status_code=404, detail="No chats found")


@router.get("/chat-display", 
    description="Display the chat history between the current user and another user.",
    response_model=ChatDisplayResponse)
async def getChat(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    receiver_id : int
):
    chat_list = chatDisplay(db=db, other_user_id=receiver_id, current_user_id=current_user.id)
    if chat_list:
        return {"chat": chat_list}
    raise HTTPException(status_code=404, detail="No chat history found")