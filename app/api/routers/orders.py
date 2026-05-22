from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import Order, Product, User
from app.schemas.shop import OrderCreate, OrderResponse
from app.core.security import get_current_user  # Імпортуємо захист

router = APIRouter(prefix="/orders", tags=["Orders"])

# 1. Створення замовлення (Тільки для авторизованих)
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Захист!
):
    # Перевірка, чи існує товар
    prod_res = await db.execute(select(Product).where(Product.id == order_data.product_id))
    product = prod_res.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Створюємо замовлення, використовуючи ID поточного користувача
    db_order = Order(
        product_id=order_data.product_id,
        user_id=current_user.id,  # ПРИВ'ЯЗКА ДО АВТОРИЗОВАНОГО ЮЗЕРА
        status="pending"
    )
    
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

# 2. Отримання власних замовлень (Тільки для авторизованих)
@router.get("/me", response_model=list[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Захист!
):
    # Отримуємо замовлення лише для того, хто зараз авторизований
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return result.scalars().all()

# 3. Отримання всіх замовлень (Адміністративна ручка - приклад)
@router.get("/", response_model=list[OrderResponse])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Захист!
):
    # Додайте перевірку, якщо у вас є роль адміна
    result = await db.execute(select(Order))
    return result.scalars().all()