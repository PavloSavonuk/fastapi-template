from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# Емуляція бази даних (звичайний словник)
users_db = {}
id_counter = 1

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global id_counter
    new_user = {**user.model_dump(), "id": id_counter}
    users_db[id_counter] = new_user
    id_counter += 1
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return users_db[user_id]

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    current_user = users_db[user_id]
    update_dict = user_data.model_dump(exclude_unset=True)
    updated_user = {**current_user, **update_dict}
    users_db[user_id] = updated_user
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    del users_db[user_id]
    return {"message": f"Користувача {user_id} видалено"}