from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table, DateTime, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from schemas import UserRole, Gender

Base = declarative_base()

# Many-to-many relationships
event_participants = Table(
    'event_participants',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

post_likes = Table(
    'post_likes',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

daily_menu_dishes = Table(
    'daily_menu_dishes',
    Base.metadata,
    Column('daily_menu_id', Integer, ForeignKey(
        'daily_menus.id'), primary_key=True),
    Column('dish_id', Integer, ForeignKey('dishes.id'), primary_key=True)
)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default=UserRole.STUDENT.value)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    # New fields
    gender = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    avatar = Column(String, nullable=True)
    selected_group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    posts = relationship("PostDB", back_populates="author")
    comments = relationship("CommentDB", back_populates="author")
    news = relationship("NewsDB", back_populates="author")
    knowledge_bases = relationship("KnowledgeBaseDB", back_populates="author")
    events_participated = relationship(
        "EventDB", secondary=event_participants, back_populates="participants")
    chat_history = relationship(
        "ChatHistoryDB", back_populates="user", uselist=False)
    selected_group = relationship("GroupDB", foreign_keys=[selected_group_id])


class KnowledgeBaseDB(Base):
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    content_type = Column(String)
    content_url = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    # Relationships
    author = relationship("UserDB", back_populates="knowledge_bases")


class EventDB(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(Float, default=0)
    max_participants = Column(Integer)
    is_team_event = Column(Boolean, default=False)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    participants = relationship(
        "UserDB", secondary=event_participants, back_populates="events_participated")
    gallery_images = relationship("GalleryImageDB", back_populates="event")


class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    # Relationships
    author = relationship("UserDB", back_populates="comments")
    post = relationship("PostDB", back_populates="comments")


class PostDB(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    # Relationships
    author = relationship("UserDB", back_populates="posts")
    comments = relationship("CommentDB", back_populates="post")
    likes = relationship("UserDB", secondary=post_likes)


class NewsDB(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    # Relationships
    author = relationship("UserDB", back_populates="news")


class GalleryImageDB(Base):
    __tablename__ = "gallery_images"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    image_url = Column(String)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    event = relationship("EventDB", back_populates="gallery_images")


class DailyMenuDB(Base):
    __tablename__ = "daily_menus"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.utcnow().date)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    # Relationships
    dishes = relationship(
        "DishDB", secondary=daily_menu_dishes, back_populates="daily_menus")


class DishDB(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    composition = Column(Text, nullable=True)
    proteins = Column(Float, nullable=True)
    fats = Column(Float, nullable=True)
    carbohydrates = Column(Float, nullable=True)
    kilocalories = Column(Float, nullable=True)
    price = Column(Float)
    photo = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey(
        "dish_categories.id"), nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    # Relationships
    category = relationship("DishCategoryDB", back_populates="dishes")
    daily_menus = relationship(
        "DailyMenuDB", secondary=daily_menu_dishes, back_populates="dishes")


class DishCategoryDB(Base):
    __tablename__ = "dish_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    dishes = relationship("DishDB", back_populates="category")


class ChatHistoryDB(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    messages = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("UserDB", back_populates="chat_history")


# Модели для расписания
class TeacherDB(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    lessons = relationship("LessonDB", secondary="lesson_teachers", back_populates="teachers")


class GroupDB(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, index=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    lessons = relationship("LessonDB", secondary="lesson_groups", back_populates="groups")


class SubjectDB(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    lessons = relationship("LessonDB", back_populates="subject")


class PlaceDB(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    lessons = relationship("LessonDB", secondary="lesson_places", back_populates="places")


# Отношения многие-ко-многим для уроков
lesson_teachers = Table(
    'lesson_teachers',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
    Column('teacher_id', Integer, ForeignKey('teachers.id'), primary_key=True)
)

lesson_groups = Table(
    'lesson_groups',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

lesson_places = Table(
    'lesson_places',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
    Column('place_id', Integer, ForeignKey('places.id'), primary_key=True)
)


class LessonDB(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    weekday = Column(Integer, index=True)
    number = Column(Integer, index=True)
    start_time = Column(String)
    end_time = Column(String)
    odd_week = Column(Boolean, default=True)
    even_week = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    subject = relationship("SubjectDB", back_populates="lessons")
    teachers = relationship("TeacherDB", secondary=lesson_teachers, back_populates="lessons")
    groups = relationship("GroupDB", secondary=lesson_groups, back_populates="lessons")
    places = relationship("PlaceDB", secondary=lesson_places, back_populates="lessons")
