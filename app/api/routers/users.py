from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import User, Profile
from app.schemas.users import UserCreate, UserResponse, ProfileCreate, ProfileResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=user_data.password + "fakehash"
    )
    db.add(db_user)
    await db.commit()
    # Після commit та refresh знову робимо запит з завантаженням профілю
    await db.refresh(db_user)
    
    # Повторний запит для правильного завантаження зв'язків через selectinload
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == db_user.id)
    )
    return result.scalar_one()

@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.profile)).offset(skip).limit(limit)
    )
    return result.scalars().all()