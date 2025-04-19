from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import UserDB
from schemas import User, UserRole
from dependencies import get_db, get_current_active_user

user_router = APIRouter(tags=["Users"])

@user_router.get("/users/me", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_active_user)):
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