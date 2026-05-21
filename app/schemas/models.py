from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileBase(BaseModel):
    bio: str | None = None
    # address у вас немає в моделі Profile, тому прибираємо його
    # phone у вас є в моделі, тому додамо його

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    bio: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None # Це поле є у вашій моделі
    profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True
        extra = "ignore"