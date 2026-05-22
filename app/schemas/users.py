from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileBase(BaseModel):
    bio: str | None = None
    phone: str | None = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None
    profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True
        extra = "ignore"

