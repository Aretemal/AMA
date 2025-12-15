from fastapi import APIRouter

from app.api.routes import articles, auth
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(auth.router)
api_router.include_router(articles.router)