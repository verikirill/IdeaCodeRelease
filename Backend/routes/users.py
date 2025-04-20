from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path

from models import UserDB
from schemas import User, UserRole, UserUpdate
from dependencies import get_db, get_current_active_user

user_router = APIRouter(tags=["Users"])

# Создаем директорию для хранения аватаров, если её нет
AVATAR_DIR = Path("static/avatars")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

@user_router.get("/users/me", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_active_user)):
    return current_user

@user_router.put("/users/update-profile", response_model=User)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Обновляет профиль текущего пользователя.
    """
    # Обновляем только разрешенные поля
    for field, value in user_data.dict(exclude_unset=True).items():
        # Проверяем, существует ли поле в модели пользователя
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@user_router.post("/users/upload-avatar", response_model=User)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Загружает аватар для текущего пользователя.
    """
    # Проверяем тип файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")
    
    # Создаем уникальное имя файла
    file_extension = os.path.splitext(file.filename)[1]
    avatar_name = f"avatar_{current_user.id}{file_extension}"
    avatar_path = AVATAR_DIR / avatar_name
    
    # Сохраняем файл
    with avatar_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Обновляем путь к аватару в базе данных
    avatar_url = f"/static/avatars/{avatar_name}"
    current_user.avatar = avatar_url
    db.commit()
    
    return current_user

@user_router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users

@user_router.get("/users/role/{role}", response_model=List[User])
async def read_users_by_role(role: UserRole, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if not current_user.is_admin and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(UserDB).filter(UserDB.role == role).all()
    return users 