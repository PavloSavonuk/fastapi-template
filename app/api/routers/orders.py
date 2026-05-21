from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import Order, Product, User
from app.schemas.shop import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    # Перевірка юзера та товару
    user_res = await db.execute(select(User).where(User.id == order_data.user_id))
    prod_res = await db.execute(select(Product).where(Product.id == order_data.product_id))
    
    if not user_res.scalars().first():
        raise HTTPException(status_code=404, detail="User not found")
    if not prod_res.scalars().first():
        raise HTTPException(status_code=404, detail="Product not found")

    db_order = Order(**order_data.model_dump(), status="pending")
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.get("/", response_model=list[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()