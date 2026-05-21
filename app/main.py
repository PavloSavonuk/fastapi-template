from fastapi import FastAPI
from app.api.routers import users, shop, orders

app = FastAPI(title="FastAPI Lab 4 Store")

app.include_router(users.router)
app.include_router(shop.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Database connected successfully!"}