from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path

from models import GalleryImageDB, EventDB, UserDB
from schemas import GalleryImage, GalleryImageCreate, UserRole
from dependencies import get_db, get_current_active_user, convert_to_db_types

gallery_router = APIRouter(prefix="/gallery", tags=["Gallery"])

UPLOAD_DIR = Path("static/uploads/gallery")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@gallery_router.get("", response_model=List[GalleryImage])
async def read_gallery_images(event_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if event_id:
        gallery_images = db.query(GalleryImageDB).filter(GalleryImageDB.event_id == event_id).offset(skip).limit(limit).all()
    else:
        gallery_images = db.query(GalleryImageDB).offset(skip).limit(limit).all()
    return gallery_images

@gallery_router.get("/{image_id}", response_model=GalleryImage)
async def read_gallery_image(image_id: int, db: Session = Depends(get_db)):
    gallery_image = db.query(GalleryImageDB).filter(GalleryImageDB.id == image_id).first()
    if gallery_image is None:
        raise HTTPException(status_code=404, detail="Gallery image not found")
    return gallery_image

@gallery_router.post("/upload", response_model=GalleryImage)
async def upload_gallery_image(
    event_id: int = Form(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admins and teachers can upload gallery images"
        )
    
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    content_type = file.content_type
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = UPLOAD_DIR / unique_filename
    
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    # Используем абсолютный URL для совместимости с валидацией URL в Pydantic
    base_url = "http://localhost:8000"  # Замените на свой базовый URL
    image_url = f"{base_url}/static/uploads/gallery/{unique_filename}"
    
    try:
        gallery_image = GalleryImageCreate(
            event_id=event_id,
            title=title or file.filename,
            description=description or "",
            image_url=image_url
        )
        
        gallery_image_dict = convert_to_db_types(gallery_image)
        
        db_gallery_image = GalleryImageDB(**gallery_image_dict)
        db.add(db_gallery_image)
        db.commit()
        db.refresh(db_gallery_image)
        
        return db_gallery_image
    except Exception as e:
        # Удаляем загруженный файл в случае ошибки
        if file_location.exists():
            os.remove(file_location)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating gallery image: {str(e)}"
        )

@gallery_router.post("", response_model=GalleryImage)
async def create_gallery_image(gallery_image: GalleryImageCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == gallery_image.event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only admins and teachers can add gallery images")
    
    gallery_image_dict = convert_to_db_types(gallery_image)
    
    db_gallery_image = GalleryImageDB(**gallery_image_dict)
    db.add(db_gallery_image)
    db.commit()
    db.refresh(db_gallery_image)
    return db_gallery_image

@gallery_router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gallery_image(image_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only admins and teachers can delete gallery images")
    
    db_gallery_image = db.query(GalleryImageDB).filter(GalleryImageDB.id == image_id).first()
    if db_gallery_image is None:
        raise HTTPException(status_code=404, detail="Gallery image not found")
    
    db.delete(db_gallery_image)
    db.commit()
    return None 