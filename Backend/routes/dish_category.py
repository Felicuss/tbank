from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import UserDB, DishCategoryDB
from schemas import UserRole, DishCategory, DishCategoryCreate
from dependencies import get_db, get_current_active_user, convert_to_db_types

category_router = APIRouter(prefix="/dish_category", tags=["Dish categories"])


@category_router.get("", response_model=List[DishCategory])
async def read_dish_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dish_categories = db.query(DishCategoryDB).offset(skip).limit(limit).all()
    return dish_categories


@category_router.get("/{dish_category_id}", response_model=DishCategory)
async def read_dish_category(dish_category_id: int, db: Session = Depends(get_db)):
    dish_category = db.query(DishCategoryDB).filter(
        DishCategoryDB.id == dish_category_id).first()
    if dish_category is None:
        raise HTTPException(status_code=404, detail="Dish category not found")
    return dish_category


@category_router.post("", response_model=DishCategory)
async def create_dish_category(dish_category: DishCategoryCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can create dish category")

    dish_category_dict = convert_to_db_types(dish_category)

    db_dish_category = DishCategoryDB(**dish_category_dict)
    db.add(db_dish_category)
    db.commit()
    db.refresh(db_dish_category)
    return db_dish_category


@category_router.put("/{dish_category_id}", response_model=DishCategory)
async def update_dish_category(dish_category_id: int, dish_category: DishCategoryCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can update dish category")

    db_dish_category = db.query(DishCategoryDB).filter(
        DishCategoryDB.id == dish_category_id).first()
    if db_dish_category is None:
        raise HTTPException(status_code=404, detail="Dish category not found")

    dish_category_dict = convert_to_db_types(dish_category)

    for key, value in dish_category_dict.items():
        setattr(db_dish_category, key, value)

    db.commit()
    db.refresh(db_dish_category)
    return db_dish_category


@category_router.delete("/{dish_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_category(dish_category_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can delete dish category")

    db_dish_category = db.query(DishCategoryDB).filter(
        DishCategoryDB.id == dish_category_id).first()
    if db_dish_category is None:
        raise HTTPException(status_code=404, detail="Dish category not found")

    db.delete(db_dish_category)
    db.commit()
    return None
