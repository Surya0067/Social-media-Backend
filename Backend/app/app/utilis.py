from db.db import SessionLocal
from models import User, OTP
from core.security import get_password_hash,getSecretKey,verify_password

from typing import Any, Dict, Optional, Union
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import random


def processForgotPassword(db: Session, identifier: str, is_email: bool):
    from curd import curd_user
    user = None
    if is_email:
        user = curd_user.getByEmail(db=db, email=identifier)
    else:
        user = curd_user.get_user(db=db, username=identifier)

    if user:
        otp = getOtp(db=db, username=user.username)
        if otp:
            return {"message": "OTP sent", "OTP": otp["otp"],"secretKey":otp["secret_key"]}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can't generate OTP"
            )
    detail_msg = "Invalid email" if is_email else "Invalid username"
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg)

def getOtp(db: Session, username : str):
    from curd.curd_user import get_user
    user = get_user(db=db,username=username)
    if user:
        random_number = random.randint(100000, 999999)
        current_time = db.query(func.now()).scalar()
        expire_time = current_time + timedelta(minutes=5)
        db.add(OTP(user_id=user.id, otp=random_number, expired_time=expire_time))
        new_secret_key =getSecretKey()
        user.secret_key = new_secret_key
        db.commit()
        return dict(otp = random_number,secret_key = new_secret_key)
    raise HTTPException(status_code=404,detail="User not found")



def getResentOtp(db: Session, secret_key : str):
    from curd.curd_user import get  # Moved import here to prevent circular import
    user = db.query(User).filter(User.secret_key == secret_key).first()
    if user:
        random_number = random.randint(100000, 999999)
        current_time = db.query(func.now()).scalar()
        expire_time = current_time + timedelta(minutes=5)
        db.add(OTP(user_id=user.id, otp=random_number, expired_time=expire_time))
        new_secret_key =getSecretKey()
        user.secret_key = new_secret_key
        db.commit()
        return dict(otp = random_number,secret_key = new_secret_key)
    raise HTTPException(status_code=404,detail="User not found")


def verifyOtp(db: Session, otp: int, secret_key : str):
    from curd.curd_user import get  # Moved import here to prevent circular import

    db_otp = db.query(OTP).join(User).filter(OTP.otp == otp,User.secret_key == secret_key).first()
    current_time = db.query(func.now()).scalar()
    if db_otp:
        user = get(db=db,user_id=db_otp.user_id)
        if (current_time <= db_otp.expired_time):
            user.is_verfied = True
            db.commit()
            return dict(message="OTP verified", status=200)
        else:
            return dict(message="OTP Expired", status=419)
    return dict(message="Invalid OTP", status=400)

def updateUserPassword(db: Session, username: str, password: str):
    change_password = db.query(User).filter(User.username == username).first()
    change_password.hashed_password = get_password_hash(password=password)
    db.commit()



def resetPassword(db: Session, secret_key: str, otp: int, newpassword: str):
    from curd.curd_user import get  # Moved import here to prevent circular import

    user = db.query(User).filter(User.secret_key == secret_key).first()
    if user:
        verify = verifyOtp(db=db, secret_key=user.secret_key, otp=otp)
        if verify["status"] == 200:
            updateUserPassword(db=db, username=user.username, password=newpassword)
            return dict(status_code=status.HTTP_200_OK, detail="Password Changed")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not found"
        )

def changePassword(db: Session, user_id: int, old_password: str, new_password: str):
    from curd.curd_user import get  # Moved import here to prevent circular import
    user = get(db=db, user_id=user_id)
    
    if user:
        db_password = user.hashed_password
        if verify_password(old_password, db_password): 
            user.hashed_password = get_password_hash(new_password)
            db.commit()
            return {"message": "Password Changed"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")