from pydantic import BaseModel
from typing import Optional

class UserName(BaseModel):
    username: Optional[str] = None
    full_name : Optional[str] = None

class UserContact(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None

class UserAccount(BaseModel):
    account_status: Optional[str] = None
    bio: Optional[str] = None