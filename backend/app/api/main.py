from fastapi import APIRouter

from app.api.routes import articles
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(articles.router)