from pydantic import BaseModel, EmailStr
from fastapi import Body
from typing import Optional,List
class UserCreate(BaseModel):
  full_name: str = Body(...,description="Full Name of the user")
  phone_number : str = Body(...,description="Phone number of the user and must be unique")
  email: EmailStr = Body(...,description="Email of the User and must be unique")
  username : str = Body(...,description="Username Must be unique")
  password: str = Body(...,description="password must be minimum 8 letters and maximum 16 letters",min_length=8,max_length=16)

class UserOut(BaseModel):
  message : str
  username : str
  otp : int
  secret_key : str

class PublicProfileResponse(BaseModel):
    username: str
    fullname: str
    bio: Optional[str]
    profile_photo: Optional[str]
    post_count: Optional[int]
    post_ids: Optional[List[int]]

class PrivateProfileResponse(BaseModel):
    username: str
    fullname: str
    profile_photo: Optional[str]