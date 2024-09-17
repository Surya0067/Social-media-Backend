from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import EmailStr
from sqlalchemy.orm import Session

from models.user import User
from api.deps import get_db
from utilis import getOtp, verifyOtp, resetPassword, getResentOtp,processForgotPassword
from schemas import UserCreate, UserOut,CommonMessage,OTPOut,ResentOTP
from curd import curd_user

router = APIRouter()


@router.post("/register", response_model=UserOut,description="To create the new user")
async def createUser(user_in: UserCreate, db: Session = Depends(get_db)):
    user = curd_user.getByEmail(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exits"
        )
    user = curd_user.get_user(db=db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exits"
        )
    user = curd_user.createUser(db=db, user=user_in)
    if user:
        return user


@router.post("/verify-otp",description="Used To verify the otp and scerect key.after user Created",response_model=CommonMessage)
async def user_verify_otp(
    secret_key: str = Body(...,description="Secret key which sent before"),
    otp: int = Body(...,description="Unique 6 digit number"),
    db: Session = Depends(get_db)
):
    verify = verifyOtp(db=db, secret_key=secret_key, otp=otp)
    return verify


@router.post("/resend-otp",description="To resent the otp",response_model=OTPOut)
async def resentOtp(*, db: Session = Depends(get_db), secret_key: ResentOTP = Body(...,description="Secret key which sent before")):
    otp = getResentOtp(db=db, secret_key=secret_key)
    if otp:
        return dict(message="otp sent successfully", otp=otp["otp"],secret_key = otp["secret_key"])


@router.post("/forgot-password",description="If the user forgot the password",response_model=OTPOut)
async def forgotPassword(
    *,
    db: Session = Depends(get_db),
    username: str | None = Body(default=None,description="Username if user selected username"),
    email: EmailStr | None = Body(default=None,description="Email if user selected Email")  
):
    if username:
        return processForgotPassword(db, identifier=username, is_email=False)
    elif email:
        return processForgotPassword(db, identifier=email, is_email=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Value not found"
        )


@router.post("/reset-password",response_model=CommonMessage,description="User can reset the otp after receving OTP")
async def user_reset_password(
    *,
    db: Session = Depends(get_db), 
    otp: int = Body(...), 
    secret_key: str = Body(...), 
    newpassword: str = Body(...)
):
    # Access the secret_key field from the Pydantic model
    result = resetPassword(
        db=db, secret_key=secret_key, newpassword=newpassword, otp=otp
    )
    return result