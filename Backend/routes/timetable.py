from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import sys
import os
import pandas as pd
import re
from datetime import datetime, date, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "../Table"))

from profcomff_parse_lib import *
from dependencies import get_db, get_admin_user, get_current_active_user
from models import TeacherDB, GroupDB, SubjectDB, PlaceDB, LessonDB, lesson_groups, lesson_teachers, lesson_places, UserDB
from schemas import UpdateTimeTable, UserGroupSelect

router = APIRouter(prefix="/timetable", tags=["Timetable"])

SOURCES = [
    [1, 1, 6], [1, 2, 6], [1, 3, 6],
    [2, 1, 6], [2, 2, 6], [2, 3, 6],
    [3, 1, 10], [3, 2, 8],
    [4, 1, 10], [4, 2, 10],
    [5, 1, 13], [5, 2, 11],
    [6, 1, 11], [6, 2, 10]
]

USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}


def clear_timetable_data(db: Session):
    db.execute(text("DELETE FROM lesson_teachers"))
    db.execute(text("DELETE FROM lesson_groups"))
    db.execute(text("DELETE FROM lesson_places"))
    
    db.query(LessonDB).delete()
    db.query(TeacherDB).delete()
    db.query(GroupDB).delete() 
    db.query(SubjectDB).delete()
    db.query(PlaceDB).delete()
    db.commit()


def fetch_and_parse_data():
    data = []
    for ind, source in enumerate(SOURCES):
        for group in range(1, source[2]+1):
            url = f'http://ras.phys.msu.ru/table/{source[0]}/{source[1]}/{group}.htm'
            response = None
            try:
                import requests as r
                response = r.get(url, headers=HEADERS)
                if response.status_code == 200:
                    data.append({
                        'url': url,
                        'raw_html': response.text,
                    })
            except Exception as e:
                continue
    
    if not data:
        return None, None, None, None, None
    
    timetables = pd.DataFrame(data)
    
    results = pd.DataFrame()
    for i, row in timetables.iterrows():
        try:
            parsed_timetable = parse_timetable(row["raw_html"])
            if not parsed_timetable.empty:
                results = pd.concat([results, parsed_timetable])
        except Exception as e:
            continue
    
    if results.empty:
        return None, None, None, None, None
    
    try:
        lessons = parse_name(results)
        lessons, places, groups, teachers, subjects = parse_all(lessons)
        
        fixed_groups = []
        for group in groups:
            number, name = group
            
            if len(number) > 5:
                clean_number = re.match(r'(\d{3}\w{0,2})', number)
                if clean_number:
                    fixed_groups.append((clean_number.group(1), name))
                else:
                    fixed_groups.append(group)
            else:
                fixed_groups.append(group)
        
        groups = fixed_groups
        
        lessons = multiple_lessons(lessons)
        lessons = flatten(lessons)
        lessons = all_to_array(lessons)
        
        return lessons, places, groups, teachers, subjects
    except Exception as e:
        return None, None, None, None, None


def save_data_to_db(db: Session, lessons, places, groups, teachers, subjects):
    teacher_map = {}
    for teacher_name in teachers:
        teacher = TeacherDB(name=teacher_name)
        db.add(teacher)
        db.flush()
        teacher_map[teacher_name] = teacher.id
    
    group_map = {}
    for group in groups:
        number, name = group
        
        clean_number = re.match(r'(\d{3}\w{0,2})', number)
        if clean_number:
            clean_number = clean_number.group(1)
        else:
            clean_number = number
            
        group_db = GroupDB(number=clean_number, name=name)
        db.add(group_db)
        db.flush()
        group_map[group] = group_db.id
    
    subject_map = {}
    for subject_name in subjects:
        subject = SubjectDB(name=subject_name)
        db.add(subject)
        db.flush()
        subject_map[subject_name] = subject.id
    
    place_map = {}
    for place_name in places:
        place = PlaceDB(name=place_name)
        db.add(place)
        db.flush()
        place_map[place_name] = place.id
    
    lesson_count = 0
    lesson_group_links = 0
    
    for _, lesson in lessons.iterrows():
        subject_id = subject_map.get(lesson['subject'])
        if not subject_id:
            continue
        
        lesson_db = LessonDB(
            subject_id=subject_id,
            weekday=lesson['weekday'],
            number=lesson['num'],
            start_time=lesson['start'],
            end_time=lesson['end'],
            odd_week=lesson['odd'],
            even_week=lesson['even']
        )
        db.add(lesson_db)
        db.flush()
        lesson_count += 1
        
        teacher_set = set()
        for teacher_name in lesson['teacher']:
            teacher_id = teacher_map.get(teacher_name)
            if teacher_id and teacher_id not in teacher_set:
                teacher_set.add(teacher_id)
                db.execute(
                    text(f"INSERT OR IGNORE INTO lesson_teachers (lesson_id, teacher_id) VALUES ({lesson_db.id}, {teacher_id})")
                )
        
        group_set = set()
        for group in lesson['group']:
            if not isinstance(group, tuple):
                group_tuple = None
                for g_tuple in group_map.keys():
                    if g_tuple[0] == group:
                        group_tuple = g_tuple
                        break
            else:
                group_tuple = group
                
            if group_tuple and group_tuple in group_map:
                group_id = group_map[group_tuple]
                if group_id and group_id not in group_set:
                    group_set.add(group_id)
                    db.execute(
                        text(f"INSERT OR IGNORE INTO lesson_groups (lesson_id, group_id) VALUES ({lesson_db.id}, {group_id})")
                    )
                    lesson_group_links += 1
        
        place_set = set()
        for place_name in lesson['place']:
            place_id = place_map.get(place_name)
            if place_id and place_id not in place_set:
                place_set.add(place_id)
                db.execute(
                    text(f"INSERT OR IGNORE INTO lesson_places (lesson_id, place_id) VALUES ({lesson_db.id}, {place_id})")
                )
    
    db.commit()


def update_timetable_task(db: Session):
    clear_timetable_data(db)
    
    lessons, places, groups, teachers, subjects = fetch_and_parse_data()
    if lessons is None:
        return
    
    analyze_parsed_data(lessons, places, groups, teachers, subjects)
    
    save_data_to_db(db, lessons, places, groups, teachers, subjects)


def analyze_parsed_data(lessons, places, groups, teachers, subjects):
    problematic_groups = []
    for group in groups:
        number, name = group
        if len(number) > 5:
            problematic_groups.append(group)
    
    lessons_without_groups = lessons[lessons['group'].apply(lambda x: len(x) == 0)]
    lessons_without_teachers = lessons[lessons['teacher'].apply(lambda x: len(x) == 0)]
    lessons_without_places = lessons[lessons['place'].apply(lambda x: len(x) == 0)]


@router.post("/update", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def update_timetable(
    background_tasks: BackgroundTasks,
    update_data: UpdateTimeTable,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_admin_user)
):
    """
    Запускает процесс обновления расписания в фоновом режиме.
    Требуются права администратора.
    """
    if update_data.force_update:
        background_tasks.add_task(update_timetable_task, db)
    else:
        background_tasks.add_task(update_timetable_task, db)
    
    return {"message": "Обновление расписания запущено"}


def get_group_lessons_simplified(
    group_id: int,
    db: Session
):
    group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {group_id} не найдена"
        )
    
    lessons = db.query(LessonDB).join(
        lesson_groups, 
        LessonDB.id == lesson_groups.c.lesson_id
    ).filter(
        lesson_groups.c.group_id == group_id
    ).order_by(
        LessonDB.weekday,
        LessonDB.number
    ).all()
    
    simplified_lessons = []
    for lesson in lessons:
        subject = db.query(SubjectDB).filter(SubjectDB.id == lesson.subject_id).first()
        
        teacher_names = []
        for teacher in lesson.teachers:
            teacher_names.append(teacher.name)
        
        place_names = []
        for place in lesson.places:
            place_names.append(place.name)
        
        simplified_lessons.append({
            "id": lesson.id,
            "subject": subject.name if subject else "Нет данных",
            "teachers": teacher_names,
            "places": place_names,
            "weekday": lesson.weekday,
            "weekday_name": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"][lesson.weekday],
            "number": lesson.number,
            "start_time": lesson.start_time,
            "end_time": lesson.end_time,
            "odd_week": lesson.odd_week,
            "even_week": lesson.even_week,
            "week_type": "Верхняя" if lesson.even_week and not lesson.odd_week else
                       "Нижняя" if lesson.odd_week and not lesson.even_week else "Обе"
        })
    
    return simplified_lessons


def get_group_lessons_by_day_simplified(
    group_id: int,
    weekday: int,
    db: Session,
    week_type: Optional[str] = None
):
    group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {group_id} не найдена"
        )
    
    if weekday < 0 or weekday > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="День недели должен быть числом от 0 (понедельник) до 6 (воскресенье)"
        )
    
    query = db.query(LessonDB).join(
        lesson_groups, 
        LessonDB.id == lesson_groups.c.lesson_id
    ).filter(
        lesson_groups.c.group_id == group_id,
        LessonDB.weekday == weekday
    )
    
    if week_type:
        if week_type.lower() == 'upper':
            query = query.filter(LessonDB.even_week == True)
        elif week_type.lower() == 'lower':
            query = query.filter(LessonDB.odd_week == True)
    
    lessons = query.order_by(LessonDB.number).all()
    
    weekday_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    
    simplified_lessons = []
    for lesson in lessons:
        subject = db.query(SubjectDB).filter(SubjectDB.id == lesson.subject_id).first()
        
        teacher_names = []
        for teacher in lesson.teachers:
            teacher_names.append(teacher.name)
        
        place_names = []
        for place in lesson.places:
            place_names.append(place.name)
        
        simplified_lessons.append({
            "id": lesson.id,
            "subject": subject.name if subject else "Нет данных",
            "teachers": teacher_names,
            "places": place_names,
            "weekday": lesson.weekday,
            "weekday_name": weekday_names[weekday],
            "number": lesson.number,
            "start_time": lesson.start_time,
            "end_time": lesson.end_time,
            "odd_week": lesson.odd_week,
            "even_week": lesson.even_week,
            "week_type": "Верхняя" if lesson.even_week and not lesson.odd_week else
                       "Нижняя" if lesson.odd_week and not lesson.even_week else "Обе"
        })
    
    return simplified_lessons


@router.get("/search_group", response_model=List[dict])
def search_group(
    query: str,
    db: Session = Depends(get_db)
):
    """
    Поиск групп по номеру.
    Возвращает список групп, соответствующих запросу.
    """
    groups = db.query(GroupDB).filter(GroupDB.number.ilike(f"%{query}%")).all()
    
    return [{"id": group.id, "number": group.number, "name": group.name} for group in groups]


@router.post("/user/select-group", response_model=dict)
async def select_user_group(
    group_data: UserGroupSelect,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Выбрать группу для текущего пользователя.
    """
    group = db.query(GroupDB).filter(GroupDB.id == group_data.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {group_data.group_id} не найдена"
        )
    
    current_user.selected_group_id = group_data.group_id
    db.commit()
    
    return {
        "message": f"Группа {group.number} ({group.name}) успешно выбрана",
        "group_id": group.id,
        "group_number": group.number,
        "group_name": group.name
    }


@router.get("/user/group", response_model=dict)
async def get_user_group(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Получить информацию о выбранной пользователем группе.
    """
    if not current_user.selected_group_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вы еще не выбрали группу"
        )
    
    group = db.query(GroupDB).filter(GroupDB.id == current_user.selected_group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {current_user.selected_group_id} не найдена"
        )
    
    return {
        "group_id": group.id,
        "group_number": group.number,
        "group_name": group.name
    }


@router.get("/user/schedule", response_model=List[dict])
async def get_user_schedule(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Получить расписание для выбранной пользователем группы на всю неделю.
    """
    if not current_user.selected_group_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вы еще не выбрали группу. Используйте /timetable/user/select-group для выбора группы."
        )
    
    return get_group_lessons_simplified(current_user.selected_group_id, db)


@router.get("/user/schedule/day/{weekday}", response_model=List[dict])
async def get_user_schedule_by_day(
    weekday: int,
    week_type: Optional[str] = Query(None, description="Тип недели: 'upper' (верхняя) или 'lower' (нижняя)"),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Получить расписание для выбранной пользователем группы на конкретный день недели.
    
    Параметры:
    - weekday: день недели (0 - понедельник, 1 - вторник, ..., 6 - воскресенье)
    - week_type: тип недели ('upper' - верхняя/четная, 'lower' - нижняя/нечетная, None - обе)
    """
    if not current_user.selected_group_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вы еще не выбрали группу. Используйте /timetable/user/select-group для выбора группы."
        )
    
    if weekday < 0 or weekday > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="День недели должен быть числом от 0 (понедельник) до 6 (воскресенье)"
        )
    
    return get_group_lessons_by_day_simplified(current_user.selected_group_id, weekday, db, week_type)


def determine_week_type(current_date=None):
    if current_date is None:
        current_date = datetime.now().date()
    
    week_number = current_date.isocalendar()[1]
    
    return 'upper' if week_number % 2 == 1 else 'lower'


@router.get("/user/schedule/today", response_model=List[dict])
async def get_user_schedule_today(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_active_user)
):
    """
    Получить расписание для выбранной пользователем группы на текущий день.
    Автоматически определяет текущий день недели и тип недели (верхняя/нижняя).
    """
    if not current_user.selected_group_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вы еще не выбрали группу."
        )
    
    today = datetime.now().date()
    weekday = today.weekday()
    week_type = determine_week_type(today)
    
    lessons = get_group_lessons_by_day_simplified(current_user.selected_group_id, weekday, db, week_type)
    
    for lesson in lessons:
        lesson["date"] = today.strftime("%d.%m.%Y")
    
    return lessons


@router.get("/group/{group_id}/today", response_model=List[dict])
async def get_group_schedule_today(
    group_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить расписание указанной группы на текущий день.
    Автоматически определяет текущий день недели и тип недели (верхняя/нижняя).
    
    Параметры:
    - group_id: идентификатор группы
    """
    group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {group_id} не найдена"
        )
    
    today = datetime.now().date()
    weekday = today.weekday()
    week_type = determine_week_type(today)
    
    lessons = get_group_lessons_by_day_simplified(group_id, weekday, db, week_type)
    
    for lesson in lessons:
        lesson["date"] = today.strftime("%d.%m.%Y")
    
    return lessons


@router.get("/group/{group_id}/tomorrow", response_model=List[dict])
async def get_group_schedule_tomorrow(
    group_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить расписание указанной группы на завтрашний день.
    Автоматически определяет день недели и тип недели (верхняя/нижняя).
    
    Параметры:
    - group_id: идентификатор группы
    """
    group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {group_id} не найдена"
        )
    
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    weekday = tomorrow.weekday()
    week_type = determine_week_type(tomorrow)
    
    lessons = get_group_lessons_by_day_simplified(group_id, weekday, db, week_type)
    
    for lesson in lessons:
        lesson["date"] = tomorrow.strftime("%d.%m.%Y")
    
    return lessons


@router.get("/group/{group_id}/schedule", response_model=List[dict])
async def get_group_full_schedule(
    group_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить полное расписание указанной группы на всю неделю.
    
    Параметры:
    - group_id: идентификатор группы
    """
    group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Группа с id {group_id} не найдена"
        )
    
    return get_group_lessons_simplified(group_id, db) 