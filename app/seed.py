import asyncio
from app.database import async_session
from app.models import User, Profile, Category, Product, Order

async def seed_data():
    # Використовуємо async_session з вашого database.py
    async with async_session() as session:
        # 1. Створюємо категорію
        category = Category(name="Electronics")
        session.add(category)
        await session.flush()  # Отримуємо ID категорії після flush

        # 2. Створюємо товар
        product = Product(title="Laptop", price=1000, category_id=category.id)
        session.add(product)

        # 3. Створюємо користувача та профіль
        user = User(username="testuser", email="test@test.com", hashed_password="password")
        session.add(user)
        await session.flush()  # Отримуємо ID користувача

        profile = Profile(bio="Hello, I love coding!", phone="123456789", user_id=user.id)
        session.add(profile)

        # 4. Створюємо замовлення
        order = Order(status="pending", user_id=user.id)
        session.add(order)

        await session.commit()
        print("База даних заповнена тестовими даними!")

if __name__ == "__main__":
    asyncio.run(seed_data())