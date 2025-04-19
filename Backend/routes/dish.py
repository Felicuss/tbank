from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import UserDB, DishDB
from schemas import UserRole, Dish, DishCreate
from dependencies import get_db, get_current_active_user, convert_to_db_types

dish_router = APIRouter(prefix="/dish", tags=["Dishes"])


@dish_router.get("", response_model=List[Dish])
async def read_dishes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishes = db.query(DishDB).offset(skip).limit(limit).all()
    return dishes


@dish_router.get("/{dish_id}", response_model=Dish)
async def read_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(DishDB).filter(
        DishDB.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@dish_router.post("", response_model=Dish)
async def create_dish(dish: DishCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can create dish")

    dish_dict = convert_to_db_types(dish)

    db_dish = DishDB(**dish_dict)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@dish_router.put("/{dish_id}", response_model=Dish)
async def update_dish(dish_id: int, dish: DishCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can update dish")

    db_dish = db.query(DishDB).filter(
        DishDB.id == dish_id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")

    dish_dict = convert_to_db_types(dish)

    for key, value in dish_dict.items():
        setattr(db_dish, key, value)

    db.commit()
    db.refresh(db_dish)
    return db_dish


@dish_router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_menu(dish_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can delete dish")

    db_dish = db.query(DishDB).filter(
        DishDB.id == dish_id).first()
    if db_dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")

    db.delete(db_dish)
    db.commit()
    return None
