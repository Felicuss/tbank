from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import EventDB, UserDB
from schemas import Event, EventCreate, UserRole
from dependencies import get_db, get_current_active_user, convert_to_db_types

event_router = APIRouter(prefix="/events", tags=["Events"])

@event_router.get("", response_model=List[Event])
async def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(EventDB).offset(skip).limit(limit).all()
    return events

@event_router.get("/{event_id}", response_model=Event)
async def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@event_router.post("", response_model=Event)
async def create_event(event: EventCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only admins and teachers can create events")
    
    event_dict = convert_to_db_types(event)
    
    db_event = EventDB(**event_dict)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@event_router.put("/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only admins and teachers can update events")
    
    db_event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_dict = convert_to_db_types(event)
    
    for key, value in event_dict.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@event_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=403, detail="Only admins and teachers can delete events")
    
    db_event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return None

@event_router.post("/{event_id}/register", response_model=Event)
async def register_for_event(event_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user in db_event.participants:
        raise HTTPException(status_code=400, detail="User already registered for this event")
    
    if len(db_event.participants) >= db_event.max_participants:
        raise HTTPException(status_code=400, detail="Event is already full")
    
    db_event.participants.append(current_user)
    db.commit()
    db.refresh(db_event)
    return db_event

@event_router.post("/{event_id}/unregister", response_model=Event)
async def unregister_from_event(event_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if current_user not in db_event.participants:
        raise HTTPException(status_code=400, detail="User is not registered for this event")
    
    db_event.participants.remove(current_user)
    db.commit()
    db.refresh(db_event)
    return db_event 