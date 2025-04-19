from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from models import CommentDB, UserDB
from schemas import Comment, CommentBase
from dependencies import get_db, get_current_active_user, convert_to_db_types

comment_router = APIRouter(prefix="/comments", tags=["Comments"])

@comment_router.put("/{comment_id}", response_model=Comment)
async def update_comment(comment_id: int, comment: CommentBase, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_comment = db.query(CommentDB).filter(CommentDB.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    comment_dict = convert_to_db_types(comment)
    
    for key, value in comment_dict.items():
        setattr(db_comment, key, value)
    
    db_comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_comment)
    return db_comment

@comment_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_comment = db.query(CommentDB).filter(CommentDB.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_comment)
    db.commit()
    return None 