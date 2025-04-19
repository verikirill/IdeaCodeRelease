from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from models import EventDB, UserDB, GalleryImageDB, event_participants
from schemas import Event, EventCreate, UserRole, User
from dependencies import get_db, get_current_active_user, convert_to_db_types
from fastapi.responses import JSONResponse
from pydantic import BaseModel

event_router = APIRouter(prefix="/events", tags=["Events"])

# Модели для запросов и ответов
class AfishaEvent(BaseModel):
    id: int
    title: str
    description: str
    image: str
    tag: str = "#Мероприятие"  # По умолчанию
    fullDescription: str
    created_at: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class EventRegistrationResponse(BaseModel):
    success: bool
    message: str
    event_id: int
    user_id: int

class EventDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    start_date: str
    end_date: str
    price: float = 0
    max_participants: int
    current_participants: int
    is_team_event: bool
    location: str
    created_at: str
    is_registered: bool = False
    
@event_router.get("/afisha", response_model=List[AfishaEvent])
async def get_afisha_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список мероприятий в формате для афиши"""
    events = db.query(EventDB).offset(skip).limit(limit).all()
    
    result = []
    for event in events:
        # Ищем изображение для события в галерее
        image = db.query(GalleryImageDB).filter(GalleryImageDB.event_id == event.id).first()
        
        # URL изображения по умолчанию, если нет в галерее
        image_url = '/event1.png'
        if image and hasattr(image, 'image_url') and image.image_url:
            image_url = image.image_url
        
        # Определяем тег на основе данных события
        tag = "#Мероприятие"
        if hasattr(event, 'location') and event.location:
            if "универсиад" in event.location.lower():
                tag = "#Универсиада"
            elif "здравниц" in event.location.lower():
                tag = "#Университетская жизнь"
        
        # Форматируем даты для фронтенда
        created_at = event.created_at.isoformat() if hasattr(event, 'created_at') and event.created_at else None
        start_date = event.start_date.isoformat() if hasattr(event, 'start_date') and event.start_date else None
        end_date = event.end_date.isoformat() if hasattr(event, 'end_date') and event.end_date else None
        
        afisha_event = {
            "id": event.id,
            "title": event.title,
            "description": event.description[:200] + "..." if len(event.description) > 200 else event.description,
            "image": image_url,
            "tag": tag,
            "fullDescription": event.description,
            "created_at": created_at,
            "start_date": start_date,
            "end_date": end_date
        }
        result.append(afisha_event)
    
    return result

@event_router.get("", response_model=List[Event])
async def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(EventDB).offset(skip).limit(limit).all()
    return events

@event_router.get("/{event_id}", response_model=EventDetailResponse)
async def read_event(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_active_user)
):
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Проверяем, зарегистрирован ли пользователь на это событие
    is_registered = False
    if current_user:
        participant = db.query(event_participants).filter_by(
            event_id=event_id, 
            user_id=current_user.id
        ).first()
        is_registered = participant is not None
    
    # Подсчет текущего количества участников
    current_participants_count = db.query(event_participants).filter_by(
        event_id=event_id
    ).count()
    
    # Форматируем даты
    created_at = event.created_at.isoformat() if hasattr(event, 'created_at') and event.created_at else None
    start_date = event.start_date.isoformat() if hasattr(event, 'start_date') and event.start_date else None
    end_date = event.end_date.isoformat() if hasattr(event, 'end_date') and event.end_date else None
    
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "start_date": start_date,
        "end_date": end_date,
        "price": event.price,
        "max_participants": event.max_participants,
        "current_participants": current_participants_count,
        "is_team_event": event.is_team_event,
        "location": event.location,
        "created_at": created_at,
        "is_registered": is_registered
    }

@event_router.post("/{event_id}/register", response_model=EventRegistrationResponse)
async def register_for_event(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_active_user)
):
    """Регистрация пользователя на событие"""
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    # Проверяем, не зарегистрирован ли пользователь уже
    participant = db.query(event_participants).filter_by(
        event_id=event_id, 
        user_id=current_user.id
    ).first()
    
    if participant:
        return {
            "success": False,
            "message": "Вы уже зарегистрированы на это событие",
            "event_id": event_id,
            "user_id": current_user.id
        }
    
    # Проверяем, не достигнуто ли максимальное количество участников
    current_participants_count = db.query(event_participants).filter_by(
        event_id=event_id
    ).count()
    
    if current_participants_count >= event.max_participants:
        return {
            "success": False,
            "message": "Достигнуто максимальное количество участников",
            "event_id": event_id,
            "user_id": current_user.id
        }
    
    # Регистрируем пользователя на событие
    statement = event_participants.insert().values(
        event_id=event_id,
        user_id=current_user.id
    )
    db.execute(statement)
    db.commit()
    
    return {
        "success": True,
        "message": "Вы успешно зарегистрированы на событие",
        "event_id": event_id,
        "user_id": current_user.id
    }

@event_router.delete("/{event_id}/register", response_model=EventRegistrationResponse)
async def unregister_from_event(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_active_user)
):
    """Отмена регистрации пользователя на событие"""
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    # Проверяем, зарегистрирован ли пользователь
    participant = db.query(event_participants).filter_by(
        event_id=event_id, 
        user_id=current_user.id
    ).first()
    
    if not participant:
        return {
            "success": False,
            "message": "Вы не были зарегистрированы на это событие",
            "event_id": event_id,
            "user_id": current_user.id
        }
    
    # Отменяем регистрацию
    statement = event_participants.delete().where(
        (event_participants.c.event_id == event_id) & 
        (event_participants.c.user_id == current_user.id)
    )
    db.execute(statement)
    db.commit()
    
    return {
        "success": True,
        "message": "Регистрация на событие отменена",
        "event_id": event_id,
        "user_id": current_user.id
    }

@event_router.get("/{event_id}/participants", response_model=List[User])
async def get_event_participants(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserDB = Depends(get_current_active_user)
):
    """Получить список участников события"""
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    # Только администраторы, преподаватели или участники события могут видеть список
    if current_user.role != UserRole.ADMIN and current_user.role != UserRole.TEACHER:
        # Проверяем, является ли пользователь участником события
        participant = db.query(event_participants).filter_by(
            event_id=event_id, 
            user_id=current_user.id
        ).first()
        
        if not participant:
            raise HTTPException(
                status_code=403, 
                detail="У вас нет прав для просмотра участников события"
            )
    
    # Получаем список участников
    users = db.query(UserDB).join(
        event_participants,
        UserDB.id == event_participants.c.user_id
    ).filter(
        event_participants.c.event_id == event_id
    ).all()
    
    return users

# Административные функции для создания/редактирования/удаления мероприятий

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