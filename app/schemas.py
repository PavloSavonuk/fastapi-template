from pydantic import BaseModel, EmailStr
from typing import Optional

# Схема для реєстрації (дані, які приходять від клієнта)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# Схема для входу (для аутентифікації)
class UserLogin(BaseModel):
    username: str
    password: str

# Схема токена, який ми повертаємо клієнту
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема для відповіді (щоб не повертати пароль в API)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True # Це дозволяє Pydantic працювати з моделями SQLAlchemy