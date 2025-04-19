from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from enum import Enum
from datetime import datetime, date


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.STUDENT
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    avatar: Optional[HttpUrl] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    avatar: HttpUrl

    class Config:
        orm_mode = True
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class KnowledgeBaseType(str, Enum):
    LECTURE = "lecture"
    MANUAL = "manual"
    ARTICLE = "article"
    VIDEO = "video"


class KnowledgeBaseBase(BaseModel):
    title: str
    description: str
    content_type: KnowledgeBaseType
    content_url: HttpUrl
    author_id: int


class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass


class KnowledgeBase(KnowledgeBaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class EventBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    price: Optional[float] = 0
    max_participants: int
    is_team_event: bool
    location: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    created_at: datetime
    participants: List[int] = []

    class Config:
        orm_mode = True
        from_attributes = True


class CommentBase(BaseModel):
    content: str
    author_id: int


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    author_id: int


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes: List[int] = []
    comments: List[Comment] = []

    class Config:
        orm_mode = True
        from_attributes = True


class NewsBase(BaseModel):
    title: str
    content: str
    author_id: int
    image_url: Optional[HttpUrl] = None


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class GalleryImageBase(BaseModel):
    event_id: int
    image_url: HttpUrl
    description: Optional[str] = None


class GalleryImageCreate(GalleryImageBase):
    pass


class GalleryImage(GalleryImageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class DailyMenuBase(BaseModel):
    date: date
    price: int
    dishes: List[int] = []


class DailyMenuCreate(DailyMenuBase):
    pass


class DailyMenu(DailyMenuBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    composition: Optional[str] = None
    proteins: Optional[float] = None
    fats: Optional[float] = None
    carbohydrates: Optional[float] = None
    kilocalories: Optional[float] = None
    price: float
    photo: Optional[str] = None
    category_id: int
    is_available: Optional[bool] = True


class DishCreate(DishBase):
    pass


class Dish(DishBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class DishCategoryBase(BaseModel):
    name: str


class DishCategoryCreate(DishCategoryBase):
    pass


class DishCategory(DishCategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class AssistantPrompt(BaseModel):
    prompt: str
    context: str


class AssistantAnswer(BaseModel):
    answer: str


class AssistantHints(BaseModel):
    hints: List[str]


class ChatHistoryBase(BaseModel):
    user_id: int
    messages: str


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistory(ChatHistoryBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# Схемы для расписания
class TeacherBase(BaseModel):
    name: str


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class GroupBase(BaseModel):
    number: str
    name: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class PlaceBase(BaseModel):
    name: str


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class LessonBase(BaseModel):
    subject_id: int
    weekday: int
    number: int
    start_time: str
    end_time: str
    odd_week: bool
    even_week: bool


class LessonCreate(LessonBase):
    teacher_ids: List[int] = []
    group_ids: List[int] = []
    place_ids: List[int] = []


class Lesson(LessonBase):
    id: int
    created_at: datetime
    teachers: List[Teacher] = []
    groups: List[Group] = []
    places: List[Place] = []
    subject: Subject

    class Config:
        orm_mode = True
        from_attributes = True


class UpdateTimeTable(BaseModel):
    force_update: bool = False


class UserGroupSelect(BaseModel):
    group_id: int

class OCRResponse(BaseModel):
    text: str
    success: bool
    file_type: str
    message: Optional[str] = None