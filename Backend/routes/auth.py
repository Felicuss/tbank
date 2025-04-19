from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

from models import UserDB
from schemas import User, UserCreate, Token, UserRole, Gender
from dependencies import get_db, get_password_hash, authenticate_user, create_access_token, get_current_user
from config import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    default_avatar = "https://example.com/avatars/default.png"
    if user.gender == Gender.MALE:
        default_avatar = "https://example.com/avatars/male.png"
    elif user.gender == Gender.FEMALE:
        default_avatar = "https://example.com/avatars/female.png"

    avatar_url = str(user.avatar) if user.avatar else default_avatar
    gender_str = user.gender.value if user.gender else None
    role_str = user.role.value
    
    db_user = UserDB(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=role_str,
        gender=gender_str,
        bio=user.bio,
        phone=user.phone,
        birth_date=user.birth_date,
        avatar=avatar_url,
        hashed_password=hashed_password,
        is_admin=True if user.role == UserRole.ADMIN else False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.get("/users/me", response_model=User)
async def get_user_me(current_user: UserDB = Depends(get_current_user)):
    return current_user 