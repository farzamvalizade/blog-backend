from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.categories.router import router as categories_router
from app.posts.router import router as posts_router
from app.site_settings.router import router as site_settings_router
from app.tags.router import router as tags_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(posts_router)
api_router.include_router(categories_router)
api_router.include_router(tags_router)
api_router.include_router(site_settings_router)
