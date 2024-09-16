from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageResponse(BaseModel):
    message: str

class ChatItemResponse(BaseModel):
    user_id: int
    username: str
    profile_image: Optional[str]
    last_message: str
    created_at: datetime

class ChatListResponse(BaseModel):
    chat_list: List[ChatItemResponse]

class ChatDetailResponse(BaseModel):
    chat_id: int
    sender_id: int
    receiver_id: int
    message: str
    created_at: datetime

class ChatDisplayResponse(BaseModel):
    chat: List[ChatDetailResponse]
