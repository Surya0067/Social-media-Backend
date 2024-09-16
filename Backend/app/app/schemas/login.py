from pydantic import BaseModel
from fastapi import Body

class CreateUserRequest(BaseModel):
  username : str
  password : str

class LoginOut(BaseModel):
  access_token : str
  token_type : str

class CommonMessage(BaseModel):
  message : str 

class ResentOTP(BaseModel):
  secret_key : str

class OTPOut(BaseModel):
  message : str
  otp : int
  secret_key : str

