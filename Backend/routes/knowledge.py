from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import KnowledgeBaseDB, UserDB
from schemas import KnowledgeBase, KnowledgeBaseCreate
from dependencies import get_db, get_current_active_user, convert_to_db_types

knowledge_router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

@knowledge_router.get("", response_model=List[KnowledgeBase])
async def read_knowledge_bases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    knowledge_bases = db.query(KnowledgeBaseDB).offset(skip).limit(limit).all()
    return knowledge_bases

@knowledge_router.get("/{knowledge_id}", response_model=KnowledgeBase)
async def read_knowledge_base(knowledge_id: int, db: Session = Depends(get_db)):
    knowledge_base = db.query(KnowledgeBaseDB).filter(KnowledgeBaseDB.id == knowledge_id).first()
    if knowledge_base is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    return knowledge_base

@knowledge_router.post("", response_model=KnowledgeBase)
async def create_knowledge_base(knowledge: KnowledgeBaseCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    knowledge_dict = convert_to_db_types(knowledge)
    db_knowledge = KnowledgeBaseDB(**knowledge_dict, author_id=current_user.id)
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

@knowledge_router.put("/{knowledge_id}", response_model=KnowledgeBase)
async def update_knowledge_base(knowledge_id: int, knowledge: KnowledgeBaseCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_knowledge = db.query(KnowledgeBaseDB).filter(KnowledgeBaseDB.id == knowledge_id).first()
    if db_knowledge is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    if db_knowledge.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    knowledge_dict = convert_to_db_types(knowledge)
    
    for key, value in knowledge_dict.items():
        setattr(db_knowledge, key, value)
    
    db_knowledge.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

@knowledge_router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_base(knowledge_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_knowledge = db.query(KnowledgeBaseDB).filter(KnowledgeBaseDB.id == knowledge_id).first()
    if db_knowledge is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    if db_knowledge.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_knowledge)
    db.commit()
    return None 