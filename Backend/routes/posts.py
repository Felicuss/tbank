from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import PostDB, UserDB, CommentDB
from schemas import Post, PostCreate, Comment, CommentBase
from dependencies import get_db, get_current_active_user, convert_to_db_types

post_router = APIRouter(prefix="/posts", tags=["Posts"])

@post_router.get("", response_model=List[Post])
async def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(PostDB).offset(skip).limit(limit).all()
    return posts

@post_router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@post_router.post("", response_model=Post)
async def create_post(post: PostCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    post_dict = convert_to_db_types(post)
    
    db_post = PostDB(**post_dict, author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@post_router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    post_dict = convert_to_db_types(post)
    
    for key, value in post_dict.items():
        setattr(db_post, key, value)
    
    db_post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return db_post

@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_post)
    db.commit()
    return None

@post_router.post("/{post_id}/like", response_model=Post)
async def like_post(post_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user in db_post.likes:
        raise HTTPException(status_code=400, detail="User already liked this post")
    
    db_post.likes.append(current_user)
    db.commit()
    db.refresh(db_post)
    return db_post

@post_router.post("/{post_id}/unlike", response_model=Post)
async def unlike_post(post_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user not in db_post.likes:
        raise HTTPException(status_code=400, detail="User has not liked this post")
    
    db_post.likes.remove(current_user)
    db.commit()
    db.refresh(db_post)
    return db_post

@post_router.post("/{post_id}/comments", response_model=Comment)
async def create_comment(post_id: int, comment: CommentBase, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment_dict = convert_to_db_types(comment)
    
    db_comment = CommentDB(**comment_dict, post_id=post_id, author_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment 