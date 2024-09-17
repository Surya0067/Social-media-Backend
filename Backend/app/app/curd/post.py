from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models import Post, ImagePostItem, Like, Comment,User,About
from schemas import PostCreate, PostDisplay, ImageDisplay
from fastapi import HTTPException, status, UploadFile
from typing import List
from curd.curd_user import get
from curd.about import get_about
import shutil, os, uuid


def get_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found or you are not the owner"
        )
    return post


def getById(db: Session, id: str):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail="Post not found"
        )
    return post


def saveImages(files: List[UploadFile], post_id: int, upload_folder: str) -> list:
    file_paths = []
    if files:
        for file in files:
            if file.content_type.startswith("image/"):
                # Generate a unique image ID
                image_id = str(uuid.uuid4())
                post_filename = f"{image_id}.jpg"
                file_path = os.path.join(upload_folder, post_filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                file_paths.append({"file_path": file_path, "image_id": image_id})
    return file_paths



def updateImages(db: Session, post_id: int, file_data: list):
    db.query(ImagePostItem).filter(ImagePostItem.post_id == post_id).update(
        {"is_active": False}, synchronize_session=False
    )
    for data in file_data:
        image_item = ImagePostItem(
            post_id=post_id, file_path=data["file_path"], image_id=data["image_id"]
        )
        db.add(image_item)
    db.commit()


def createPost(db: Session, post_create: PostCreate) -> Post:
    post = Post(caption=post_create.caption, user_id=post_create.user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def updatePost(db: Session, post: Post, caption: str):
    post.caption = caption
    post.updated_time = func.now()
    db.commit()
    db.refresh(post)
    return post


def addNewImages(db: Session, post_id: int, file_data: list):
    for data in file_data:
        image_item = ImagePostItem(
            post_id=post_id, file_path=data["file_path"], image_id=data["image_id"]
        )
        db.add(image_item)
    db.commit()


def createPostDisplay(post: Post, db: Session) -> PostDisplay:
    about = get_about(db=db, user_id=post.user_id)

    # Filter images to include only those where is_active is True
    images = [
        ImageDisplay(image_id=imagepostitem.image_id, path=imagepostitem.file_path)
        for imagepostitem in post.imagepostitems
        if imagepostitem.is_active
    ]

    return PostDisplay(
        id=post.id,
        user_id=post.user_id,
        username=post.user.username,
        profile_image=about.profile_photo,
        caption=post.caption,
        post_time=str(post.post_time),
        image=images if images else None,  # Return None if no active images
    )


def displayPost(db: Session, post_id: int):
    post = (
        db.query(Post).join(About,About.user_id == Post.user_id).filter(and_(Post.id == post_id, Post.is_active == True, About.account_status == "public")).first()
    )
    about = get_about(db=db,user_id=post.user_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found"
        )
    return createPostDisplay(post, db)


def displayRecentPost(db: Session):
    posts = (
        db.query(Post).join(About,About.user_id == Post.user_id).filter(Post.is_active == 1,About.account_status =="public").order_by(Post.post_time.desc()).all()
    )
    if posts:
        return [createPostDisplay(post, db) for post in posts]


def disablePost(db: Session, post_id: int, user_id: int):
    post = (
        db.query(Post)
        .join(ImagePostItem)
        .filter(Post.id == post_id, Post.user_id == user_id)
        .first()
    )
    if post:
        post.is_active = False
        db.commit()
        db.refresh(post)
        return dict(message="Post deleted")
    raise HTTPException(status_code=404, detail="Post not found")


def disableImages(db: Session, post_id:int,image_ids: list[str]):
    post = getById(db=db,id=post_id)
    if post:
        image = (
        db.query(ImagePostItem)
        .filter(ImagePostItem.image_id.in_(image_ids))
        .update({"is_active": False}, synchronize_session=False)
    )
        db.commit()
        return dict(message = "Image deleted")
    raise HTTPException(status_code=404,detail="Post Not found")



def addLike(db: Session, post_id: int, user_id: int):
    post = getById(db=db, id=post_id)
    if post:
        db.add(Like(post_id=post_id, user_id=user_id, liked_time=func.now()))
        db.commit()
        return dict(message="Like added")
    return HTTPException(status_code=404, detail="post not found")


def postUnlike(db: Session, post_id: int, user_id: int):
    post = getById(db=db, id=post_id)
    like = db.query(Like).filter(Like.post_id == post_id,Like.user_id == user_id).all()
    if not like:
        raise HTTPException(status_code=404,detail="User didnt liked this")
    if post:
        db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).delete(
            synchronize_session=False
        )
        db.commit()
        return dict(message="Unliked")
    return HTTPException(status_code=404, detail="post not found")


def likeCount(db: Session, post_id: int):
    post = getById(db=db, id=post_id)
    if post:
        count = db.query(Like).filter(Like.post_id == post_id).count()
        return dict(post_id=post_id, like_count=count)
    return HTTPException(status_code=404, detail="post not found")


def recentLikeBy(db: Session, post_id: int):
    post = getById(db=db, id=post_id)
    if post:
        recent_like = (
            db.query(Like)
            .filter(Like.post_id == post_id)
            .order_by(Like.liked_time.desc())
            .first()
        )
        user = db.query(User).filter(User.id == post.user_id).first()
        return dict(username=user.username)
    return HTTPException(status_code=404, detail="post not found")


def listOfLike(db: Session, post_id: int):
    post = getById(db=db, id=post_id)
    if post:
        recent_likes = (
            db.query(Like)
            .filter(Like.post_id == post_id)
            .order_by(Like.liked_time.desc())
            .all()
        )
        usernames = [like.user.username for like in recent_likes]
        return dict(post_id=post_id, usernames=usernames)
    raise HTTPException(status_code=404, detail="post not found")

def postComment(db: Session, post_id: int, user_id: int, text: str):
    post = getById(db=db, id=post_id)
    if post:
        db.add(
            Comment(
                post_id=post_id, user_id=user_id, text=text, commented_time=func.now()
            )
        )
        db.commit()
        return dict(message="comment added")
    raise HTTPException(status_code=404, detail="post not found")

def postDeleteComment(db: Session, post_id: int, comment_id: int):
    post = getById(db=db, id=post_id)
    comment = db.query(Comment).filter(Comment.post_id == post_id,Comment.id == comment_id).all()
    if not comment:
        raise HTTPException(status_code=404,detail="User didnt Comment this")
    if post:
        db.query(Comment).filter(
            Comment.post_id == post_id, Comment.id == comment_id
        ).delete(synchronize_session=False)
        db.commit()
        return dict(message="Comment Deleted")
    raise HTTPException(status_code=404, detail="post not found")

def postUpdateComment(
    db: Session, post_id: int, user_id: int, comment_id: int, text: str
):
    post = getById(db=db, id=post_id)
    comment = db.query(Comment).filter(Comment.post_id == post_id,Comment.id == comment_id).all()
    if not comment:
        raise HTTPException(status_code=404,detail="User didnt Comment this")
    if post:
        comment = (
            db.query(Comment)
            .filter(
                Comment.id == comment_id,
                Comment.post_id == post_id,
                Comment.user_id == user_id,
            )
            .first()
        )
        if comment:
            comment.text = text
            db.commit()
            db.refresh(comment)
            return dict(message="Comment Updated")

        raise HTTPException(status_code=404, detail="Comment Not Found")
    raise HTTPException(status_code=404, detail="post not found")

def commentCount(db: Session, post_id: int):
    post = getById(db=db, id=post_id)
    if post:
        count = db.query(Comment).filter(Comment.post_id == post_id).count()
        return dict(post_id=post_id, comment_count=count)
    raise HTTPException(status_code=404, detail="post not found")



def listOfComment(db: Session, post_id: int):
    post = getById(db=db, id=post_id)
    if post:
        comments = (
            db.query(Comment)
            .filter(Comment.post_id == post_id)
            .order_by(Comment.commented_time.desc())
            .all()
        )
        comment_details = [
            {"username": comment.user.username, "text": comment.text} 
            for comment in comments
        ]
        return dict(post_id=post_id, comments=comment_details)
    raise HTTPException(status_code=404, detail="post not found")


def postCount(db:Session,user_id : int):
    count = db.query(Post).filter(Post.user_id == user_id,Post.is_active == True).count()
    if count:
        return dict(post_count=count)
    return dict(post_count = 0)

def userPostList(db:Session,user_id : int):
    posts = db.query(Post).filter(Post.user_id == user_id,Post.is_active == True).all()
    if posts:
        post_ids = [post.id for post in posts]
        return {"post_ids": post_ids}
    return dict(post_ids = None)