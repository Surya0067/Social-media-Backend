from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    Form,
    status,
    Body,
    Query,
    Path,
)
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_user
from models import User, Post, ImagePostItem
from schemas import (
    PostCreate,
    PostDisplay,
    ListPostDisplay,
    CommonMessage,
    LikeResponse,
    LikesListResponse,
    CommentCountResponse,
    CommentResponse,
    CommentsListResponse,
    PostCountResponse,
    PostListResponse,
)
from core.config import settings
from curd.post import (
    get_post,
    getById,
    createPost,
    displayPost,
    displayRecentPost,
    saveImages,
    updateImages,
    updatePost,
    addNewImages,
    disablePost,
    disableImages,
    addLike,
    postUnlike,
    listOfLike,
    likeCount,
    recentLikeBy,
    postComment,
    postUpdateComment,
    postDeleteComment,
    commentCount,
    listOfComment,
)
from typing import List
import os

router = APIRouter()

UPLOAD_FOLDER = settings.POST_IMAGE_DIR
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post(
    "/create-post", description="To create a post", response_model=CommonMessage
)
async def createPostEndpoint(
    caption: str | None = Form(default=None, description="caption of the post"),
    files: List[UploadFile] | None = File(
        default=[], description="User can upload multiple image in a single post"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = createPost(db, PostCreate(caption=caption, user_id=current_user.id))

    # Save the images and associate them with the post
    if files:
        file_data = saveImages(files, post.id, UPLOAD_FOLDER)
        if file_data:
            updateImages(db, post.id, file_data)
    return {"message": "Post created successfully"}


# API to update a post and add new images without deleting old ones
@router.put(
    "/add-image/{post_id}",
    response_model=CommonMessage,
    description="User can add an image to an existing post",
)
async def addImagesToPost(
    post_id: int,
    caption: str | None = Form(
        default=None, description="if caption change for the post then mention it"
    ),
    files: List[UploadFile]  = File(...,
        description="User can add multiple image to a post with deleting the exitsing image in post",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post(db=db,user_id=current_user.id,post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found or you are not the owner"
        )
    if caption:
       updatePost(db, post, caption)

    if files:
        file_data = saveImages(files, post_id, UPLOAD_FOLDER)
        if file_data:
            addNewImages(db, post_id, file_data)

    return {"message": "Post updated successfully"}


# API to update a post, delete selected images, and add new ones
@router.put(
    "/update-images/{post_id}",
    description="User can edit the post by adding or deleting multiple image ",
    response_model=CommonMessage,
)
async def updateImagesInPost(
    post_id: int,
    caption: str | None = Form(
        default=None,
        description="if user update the caption mention it or make as null",
    ),
    files: List[UploadFile] | None = File(
        default=[], description="User can make changes to post by replacing it"
    ),
    delete_image_UUIDS: List[str] | None = Form(
        default=[], description="mention the image uuid for making changes"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post(db=db, user_id=current_user.id, post_id=post_id)


    if caption is not None:
        updatePost(db, post, caption)
    if caption is None:
        post.caption = post.caption
        db.commit()

    # If delete_image_ids are UUIDs, filter by image_id instead of id
    if delete_image_UUIDS:
        disableImages(db=db, image_ids=delete_image_UUIDS)

    if files:
        file_data = saveImages(files, post_id, UPLOAD_FOLDER)
        if file_data:
            updateImages(db, post_id, file_data)

    return {"message": "Post updated successfully"}


@router.get(
    "/show-post/{post_id}",
    description="displaying the particular image",
    response_model=PostDisplay,
)
async def showPost(
    post_id: int = Path(..., description="post id to view the image"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = displayPost(db=db, post_id=post_id)
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found"
        )


@router.get(
    "/list-post",
    description="list of post to display with the user",
    response_model=ListPostDisplay,
)
async def listPost(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    posts = displayRecentPost(db=db)
    if posts:
        return ListPostDisplay(post=posts)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )


@router.patch(
    "/delete-post/{post_id}", description="Deleting Whole Image", response_model=CommonMessage
)
async def deletePost(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    post_id: int = Path(..., description="To delete a paticular post")
):
    post = disablePost(db=db, post_id=post_id, user_id=current_user.id)
    return post


@router.patch(
    "/delete-image/{post_id}",
    response_model=CommonMessage,
    description="we can delete multiple images or single image in a paticular post",
)
async def deleteImages(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    post_id: int = Path(..., description="metion the post id to delete the images"),
    image_uuid: List[str] = Body(
        ..., description="metion the image uuid to delete the image"
    )
):
    image = disableImages(db=db, post_id=post_id, image_ids=image_uuid)
    return image


@router.post(
    "/post-like/{post_id}",
    description="To add a Like to a post",
    response_model=CommonMessage,
)
async def like(
    post_id: int = Path(..., description="Post id of the user liked"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = addLike(db=db, post_id=post_id, user_id=current_user.id)
    return like


@router.post(
    "/post-unlike/{post_id}",
    description="To add a unlike to a post",
    response_model=CommonMessage,
)
async def unlike(
    *,
    post_id: int = Path(..., description="Post id of the user unliked"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like = postUnlike(db=db, post_id=post_id, user_id=current_user.id)
    return like


@router.get(
    "/recent-like/{post_id}",
    description="Get the most recent like on a post.",
    response_model=LikeResponse,
)
async def recentLike(
    post_id: int = Path(..., description="Post id to get the last liked by"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recent_like = recentLikeBy(db=db, post_id=post_id)
    return recent_like


@router.get(
    "/total-like-username/{post_id}",
    description="Get a list of usernames who liked a specific post.",
    response_model=LikesListResponse,
)
async def totalLikeUser(
    post_id: int = Path(..., description="Post id to get the list of username"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recent_like = listOfLike(db=db, post_id=post_id)
    return recent_like


@router.get(
    "/like-count/{post_id}",
    description="Get the total number of likes on a post.",
    response_model=PostCountResponse,
)
async def totalLike(
    post_id: int = Path(..., description="Post id to get the count of like"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recent_like = likeCount(db=db, post_id=post_id)
    return recent_like


@router.post(
    "/post-comment/{post_id}",
    description="Add a comment to a post.",
    response_model=CommentResponse,
)
async def comment(
    post_id: int = Path(..., description="Post id of the user commented"),
    text: str = Body(..., description="Comment in 255 chararter is the limit"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = postComment(db=db, post_id=post_id, user_id=current_user.id, text=text)
    return comment


@router.post(
    "/post-uncomment/{post_id}",
    description="Delete your comment from a post.",
    response_model=CommentResponse,
)
async def deleteComment(
    post_id: int = Path(..., description="Postid which user deleted the comment"),
    comment_id: int = Body(
        ..., description="Comment id of the user deleted the comment"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = postDeleteComment(db=db, comment_id=comment_id, post_id=post_id)
    return comment


@router.patch(
    "/post-editcomment/{post_id}",
    description="Edit your comment on a post.",
    response_model=CommentResponse,
)
async def updateComment(
    post_id: int = Path(..., description="post id of the user edited the comment"),
    comment_id: int = Body(..., description="Comment id of the user edited"),
    text: str = Body(..., description="Text of the comment"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = postUpdateComment(
        db=db,
        post_id=post_id,
        user_id=current_user.id,
        comment_id=comment_id,
        text=text,
    )
    return response


@router.get(
    "/comment-count/{post_id}",
    description="Get the total number of comments on a post.",
    response_model=CommentCountResponse,
)
async def totalCommentCount(
    post_id: int = Path(
        ..., description="enter the post id to get the total count of comments"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = commentCount(db=db, post_id=post_id)
    return comment


@router.get(
    "/display-comment/{post_id}",
    description="Display all comments on a post.",
    response_model=CommentsListResponse,
)
async def displayComment(
    post_id: int = Path(..., description="enter the post id to display the comments"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = listOfComment(db=db, post_id=post_id)
    return comment
