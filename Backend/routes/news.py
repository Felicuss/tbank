from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import NewsDB, UserDB
from schemas import News, NewsCreate, UserRole
from dependencies import get_db, get_current_active_user, convert_to_db_types

news_router = APIRouter(prefix="/news", tags=["News"])

@news_router.get("", response_model=List[News])
async def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = db.query(NewsDB).offset(skip).limit(limit).all()
    return news

@news_router.get("/{news_id}", response_model=News)
async def read_news_item(news_id: int, db: Session = Depends(get_db)):
    news_item = db.query(NewsDB).filter(NewsDB.id == news_id).first()
    if news_item is None:
        raise HTTPException(status_code=404, detail="News item not found")
    return news_item

@news_router.post("", response_model=News)
async def create_news(news: NewsCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only admins and teachers can create news")
    
    news_dict = convert_to_db_types(news)
    
    db_news = NewsDB(**news_dict, author_id=current_user.id)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@news_router.put("/{news_id}", response_model=News)
async def update_news(news_id: int, news: NewsCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_news = db.query(NewsDB).filter(NewsDB.id == news_id).first()
    if db_news is None:
        raise HTTPException(status_code=404, detail="News item not found")
    if db_news.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    news_dict = convert_to_db_types(news)
    
    for key, value in news_dict.items():
        setattr(db_news, key, value)
    
    db_news.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_news)
    return db_news

@news_router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(news_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_news = db.query(NewsDB).filter(NewsDB.id == news_id).first()
    if db_news is None:
        raise HTTPException(status_code=404, detail="News item not found")
    if db_news.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_news)
    db.commit()
    return None 