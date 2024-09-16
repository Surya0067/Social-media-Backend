from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from schemas import UserCreate, UserOut
from models import User
from core.security import get_password_hash,getSecretKey
from utilis import getOtp


def getByEmail(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()



def createUser(db: Session, user: UserCreate):
    new_user = User(
            full_name=user.full_name,
            phone_number=user.phone_number,
            email=user.email,
            username=user.username,
            hashed_password=get_password_hash(password=user.password),
            secret_key = getSecretKey()

        )
    db.add(
        new_user
    )
    otp = getOtp(db=db, username=user.username)
    db.commit()
    return UserOut(
        message = "User Created",
        username=user.username,
        otp=otp["otp"],
        secret_key= otp["secret_key"]
    )


def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
