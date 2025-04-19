from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import DailyMenuDB, UserDB, DishDB
from schemas import DailyMenu, DailyMenuCreate, UserRole
from dependencies import get_db, get_current_active_user, convert_to_db_types, convert_daily_menu_to_schema
menu_router = APIRouter(prefix="/menu", tags=["Menu"])


@menu_router.get("", response_model=List[DailyMenu])
async def read_daily_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    daily_menus = db.query(DailyMenuDB).offset(skip).limit(limit).all()

    return [convert_daily_menu_to_schema(daily_menu) for daily_menu in daily_menus]


@menu_router.get("/{daily_menu_id}", response_model=DailyMenu)
async def read_daily_menu(daily_menu_id: int, db: Session = Depends(get_db)):
    daily_menu = db.query(DailyMenuDB).filter(
        DailyMenuDB.id == daily_menu_id).first()
    if daily_menu is None:
        raise HTTPException(status_code=404, detail="Daily menu not found")
    return convert_daily_menu_to_schema(daily_menu)


@menu_router.post("", response_model=DailyMenu)
async def create_daily_menu(daily_menu: DailyMenuCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can create daily menu")

    daily_menu_dict = convert_to_db_types(daily_menu)
    dishes_ids = daily_menu_dict.pop('dishes', [])

    db_daily_menu = DailyMenuDB(**daily_menu_dict)

    if dishes_ids:
        dishes = db.query(DishDB).filter(DishDB.id.in_(dishes_ids)).all()
        found_ids = {dish.id for dish in dishes}
        missing_ids = set(dishes_ids) - found_ids

        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Dishes with IDs {missing_ids} not found"
            )

        db_daily_menu.dishes = dishes

    db.add(db_daily_menu)
    db.commit()
    db.refresh(db_daily_menu)

    return convert_daily_menu_to_schema(db_daily_menu)


@menu_router.put("/{daily_menu_id}", response_model=DailyMenu)
async def update_daily_menu(daily_menu_id: int, daily_menu: DailyMenuCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can update daily menu")

    db_daily_menu = db.query(DailyMenuDB).filter(
        DailyMenuDB.id == daily_menu_id).first()
    if db_daily_menu is None:
        raise HTTPException(status_code=404, detail="Daily menu not found")

    daily_menu_dict = convert_to_db_types(daily_menu)
    dishes_ids = daily_menu_dict.pop('dishes', [])

    for key, value in daily_menu_dict.items():
        setattr(db_daily_menu, key, value)

    if dishes_ids:
        dishes = db.query(DishDB).filter(DishDB.id.in_(dishes_ids)).all()
        found_ids = {dish.id for dish in dishes}
        missing_ids = set(dishes_ids) - found_ids

        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Dishes with IDs {missing_ids} not found"
            )

        db_daily_menu.dishes = dishes

    db.commit()
    db.refresh(db_daily_menu)
    return convert_daily_menu_to_schema(db_daily_menu)


@menu_router.delete("/{daily_menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_menu(daily_menu_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403, detail="Only admins and teachers can delete daily menu")

    db_daily_menu = db.query(DailyMenuDB).filter(
        DailyMenuDB.id == daily_menu_id).first()
    if db_daily_menu is None:
        raise HTTPException(status_code=404, detail="Daily menu not found")

    db.delete(db_daily_menu)
    db.commit()
    return None
