from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

# 1. Імпортуємо engine та Base
from app.database import engine, Base
# 2. ОБОВ'ЯЗКОВО імпортуємо всі моделі, щоб вони зареєструвалися в Base
from app import models 
# 3. Імпортуємо роутери
from app.api.routers import users, auth, orders, shop

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код запуску: створення таблиць
    print("Спроба підключення до БД та створення таблиць...")
    retries = 10
    while retries > 0:
        try:
            async with engine.begin() as conn:
                # Ця команда створює таблиці на основі імпортованих моделей
                await conn.run_sync(Base.metadata.create_all)
            print("Успішне підключення та створення таблиць!")
            break
        except Exception as e:
            retries -= 1
            print(f"База ще не готова, чекаю 5 секунд... (залишилося {retries} спроб). Помилка: {e}")
            await asyncio.sleep(5)
    else:
        raise Exception("Не вдалося підключитися до бази даних.")
    
    yield
    
    # Код зупинки
    print("Додаток зупиняється")

# Ініціалізація FastAPI
app = FastAPI(lifespan=lifespan)

# Підключення роутерів
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(shop.router)
app.include_router(users.router)