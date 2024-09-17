from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from models import About, User
from curd.curd_user import get,get_user
from schemas.about import UserName, UserAccount, UserContact


def get_about(db: Session, user_id: str):
    about = db.query(About).filter(About.user_id == user_id).first()
    return about


def viewUser(db: Session, username: str):
    user = get_user(db=db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    about = get_about(db=db, user_id=user.id)
    if about:
        from curd.post import postCount, userPostList
        post_count = postCount(db=db, user_id=user.id)
        post_ids = userPostList(db=db, user_id=user.id)
        if about.account_status == "private":
            return {
                "username": user.username,
                "fullname": user.full_name,
                "profile_photo": about.profile_photo if about else None,
            }
        return {
            "username": user.username,
            "fullname": user.full_name,
            "bio": about.bio if about else None,
            "profile_photo": about.profile_photo if about else None,
            "post_count": post_count,
            "post_ids": post_ids,
        }
    return {"username": user.username, "full_name": user.full_name }


def updateName(db: Session, user_id: int, user_update: UserName):
    user = get(db=db, user_id=user_id)
    if not user:
        return None

    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.username is not None:
        user.username = user_update.username

    db.commit()
    db.refresh(user)
    return {"message": "Name information updated"}


def updateContact(db: Session, user_id: int, user_update: UserContact):
    user = get(db=db, user_id=user_id)
    if not user:
        return None

    if user_update.phone_number is not None:
        user.phone_number = user_update.phone_number
    if user_update.email is not None:
        user.email = user_update.email

    db.commit()
    db.refresh(user)
    return {"message": "Contact information updated"}


def updateAccount(db: Session, user_id: int, user_update: UserAccount):
    user = get(db=db, user_id=user_id)
    if not user:
        return None

    about = get_about(db=db, user_id=user.id)
    print(about.bio)
    if about is None:
        db.add(
            About(
                account_status=user_update.account_status,
                bio=user_update.bio,
                user_id=user.id,
            )
        )
    else:
        if user_update.account_status is not None:
            account_status = user_update.account_status.lower()
            if account_status in ["private", "public"]:
                about.account_status = account_status
        if user_update.bio is not None:
            about.bio = user_update.bio
        about.updated_at = func.now()

    db.commit()
    db.refresh(about)
    return {"message": "Account information updated"}


def update_user_profile_photo(db: Session, user_id: str, profile_photo_path: str):
    about = get_about(db=db, user_id=user_id)
    if not about:
        return None

    if about:
        about.profile_photo = profile_photo_path
        about.updated_at = func.now()
    else:
        new_about = About(profile_photo=profile_photo_path, user_id=user_id)
        db.add(new_about)
        about = new_about

    db.commit()
    db.refresh(about)
    return {"message": "Profile photo updated"}
