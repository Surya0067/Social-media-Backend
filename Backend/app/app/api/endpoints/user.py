from fastapi import APIRouter, Body, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_user
from models import User
from schemas import UserContact,UserAccount,UserName,CommonMessage,PrivateProfileResponse,PublicProfileResponse
from curd.about import updateAccount,updateContact,updateName, update_user_profile_photo, viewUser
from core.config import settings
from pathlib import Path
from typing import Optional,Union
from utilis import changePassword


router = APIRouter()

# Define the directory where the images will be saved
profile_image_dir = Path(settings.PROFILE_IMAGE_DIR)


@router.put("/update-names",description="User can update username and fullname",response_model=CommonMessage)
async def updateUserNames(
    user_update: UserName,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = updateName(
        db=db, user_id=current_user.id, user_update=user_update
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user

@router.put("/update-contacts",description="User can update phone number and email",response_model=CommonMessage)
async def updateUserContact(
    user_update: UserContact,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = updateContact(
        db=db, user_id=current_user.id, user_update=user_update
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user

@router.put("/update-account",description="User can update Account status like private and public and Bio",response_model=CommonMessage)
async def updateUserAccount(
    user_update: UserAccount,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = updateAccount(
        db=db, user_id=current_user.id, user_update=user_update
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user


@router.put("/upload-profile-photo",description="User can update their profile",response_model=CommonMessage)
async def upload_profile_photo(
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile_image_dir.mkdir(parents=True, exist_ok=True)

    file_extension = profile_photo.filename.split(".")[-1]

    image_filename = f"{current_user.id}_profile.{file_extension}"
    image_path = profile_image_dir / image_filename

    try:
        with open(image_path, "wb") as buffer:
            buffer.write(await profile_photo.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save profile photo",
        )

    updated_user = update_user_profile_photo(
        db=db,
        user_id=current_user.id,
        profile_photo_path=str(image_path.relative_to(settings.BASE_DIR)),
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user


@router.put("/change-password",description="User can update thier password with old password",response_model=CommonMessage)
async def userChangepassword(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    old_password: str,
    new_password: str,
):
    result = changePassword(
        db=db, user_id=user.id, old_password=old_password, new_password=new_password
    )
    return result


@router.post("/view-other/{username}",description="User can search the other user with username",response_model=PublicProfileResponse)
async def viewProfile(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_profile = viewUser(db=db, username=username)
    if user_profile:
        if user_profile.get("profile_photo"):
            user_profile["profile_photo"] = str(
                settings.BASE_DIR / user_profile["profile_photo"]
            )
        return user_profile

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
