from pydantic import BaseModel
from typing import List, Optional

class PostCreate(BaseModel):
    caption: Optional[str] = None
    user_id: int

class ImageDisplay(BaseModel):
    image_id : str
    path : str

class PostDisplay(BaseModel):
    id : int
    user_id : int
    username : str
    profile_image : str | None
    caption : str | None
    post_time :str
    image: Optional[List[ImageDisplay]]

class ListPostDisplay(BaseModel):
    post : List[PostDisplay]

class LikeResponse(BaseModel):
    username: str

class LikesListResponse(BaseModel):
    post_id: int
    usernames: List[str]

class CommentResponse(BaseModel):
    message: str

class CommentsListResponse(BaseModel):
    post_id: int
    comments: List[dict]

class CommentCountResponse(BaseModel):
    post_id: int
    comment_count: int

class PostCountResponse(BaseModel):
    post_count: int

class PostListResponse(BaseModel):
    post_ids: Optional[List[int]] = None