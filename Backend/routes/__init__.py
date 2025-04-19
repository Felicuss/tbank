from fastapi import APIRouter

from routes.auth import auth_router
from routes.users import user_router
from routes.knowledge import knowledge_router
from routes.events import event_router
from routes.posts import post_router
from routes.comments import comment_router
from routes.news import news_router
from routes.gallery import gallery_router
from routes.menu import menu_router
from routes.dish import dish_router
from routes.dish_category import category_router
from routes.assistant import assistant_router
from routes.timetable import router as timetable_router
# from routes.ocr import router as ocr_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(knowledge_router)
api_router.include_router(event_router)
api_router.include_router(post_router)
api_router.include_router(comment_router)
api_router.include_router(news_router)
api_router.include_router(gallery_router)
api_router.include_router(menu_router)
api_router.include_router(dish_router)
api_router.include_router(category_router)
api_router.include_router(assistant_router)
api_router.include_router(timetable_router)
# api_router.include_router(ocr_router)
